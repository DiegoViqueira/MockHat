"""EvaluateDB"""
import asyncio
import json
import logging
import re

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

from app.enums.deployment import Deployment
from app.enums.provider import Provider
from app.enums.level import Level
from app.enums.institution import Institution
from app.factories.grammar_prompt_factory import GrammarExtraPromptFactory
from app.factories.grammar_reference_factory import GrammarReferenceFactory
from app.models.writing_ai_chain_feedback import WritingAIChainFeedback
from app.enums.writing_task import WritingTask
from app.chains.writing_correction_chain import WritingCorrectionChain
from app.chains.grammar_correction_chain import GrammarCorrectionChain
from app.factories.few_shot_factory import FewShotWritingFactory
from app.factories.rubric_factory import RubricFactory
from app.factories.language_model_factory import LanguageModelFactory, ModelEngine

from app.core.settings import settings


logging.basicConfig(level=logging.INFO)


async def process_grammar_correction(model: ModelEngine, text: str, level: Level, institution: Institution) -> str:
    """Process a grammar correction and returns the correction.

    Args:
        text: Text to correct
        level: Level of the text
    """
    grammar_reference_factory = GrammarReferenceFactory()
    grammar_reference = grammar_reference_factory.get_grammar_reference(
        institution, level)
    extra_prompt = GrammarExtraPromptFactory().get(level)
    grammar_correction_chain = GrammarCorrectionChain(model=model)
    return await grammar_correction_chain.run(text, extra_prompt, grammar_reference)


async def process_writing(model: ModelEngine, level: Level, institution: Institution, task: WritingTask, task_value: str, task_answer: str):
    """Procesa una escritura y devuelve la corrección.

        Args:
            text: Texto a corregir
            level: Nivel de la escritura
            institution: Institución de la escritura
            task: Tarea de la escritura
            rubric: Rubrica de la escritura
            grammar_correction: Corrección de gramática
            task_value: Valor de la tarea
            task_answer: Tarea y respuesta a evaluar
            examples: Ejemplos de escritura
        """
    writing_correction_chain = WritingCorrectionChain(model=model)
    few_shot_writing_factory = FewShotWritingFactory()
    rubric_factory = RubricFactory()

    institution_enum = Institution(institution)
    level_enum = Level(level)
    task_enum = WritingTask(task)

    rubric = rubric_factory.get_rubric(
        institution_enum, level_enum, task_enum)

    logging.info("Processing writing for level: %s, institution: %s, task: %s",
                 level, institution, task)

    grammar_correction, _ = await process_grammar_correction(
        model, task_answer, level_enum, institution_enum)
    examples = few_shot_writing_factory.get_few_shot_prompt(
        institution_enum, level_enum, task_enum)

    if grammar_correction is not None:
        grammar_correction_string = grammar_correction.to_string()
    else:
        grammar_correction_string = ""

    result, _ = await writing_correction_chain.run(level_enum, institution_enum, task_enum, rubric, grammar_correction_string, task_value, task_answer, count_words(task_value), examples)

    return result


def count_words(text: str) -> int:
    """Count the number of words in a text, ignoring punctuation."""
    text = str(text)  # convertir cualquier input a string
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return len(cleaned_text.split())


async def process(df: pd.DataFrame, evaluation_data: dict, models: list[dict]):
    """Process the data from the csv file."""

    for index, row in df.iterrows():
        logging.info("Processing row %d of %d", index, len(df))
        task_value = row['question']
        task_answer = row['answer']
        level = Level(row['Level'])
        institution = Institution(row['Institution'])
        task = WritingTask(row['Task'])
        criteria_0 = "Content"
        criteria_1 = "Communicative Achievement"
        criteria_2 = "Organisation"
        criteria_3 = "Language"
        teacher_score_criteria_0 = row['Content'] if row['Content'] is not None else 0
        teacher_score_criteria_1 = row['Communicative Achievement'] if row['Communicative Achievement'] is not None else 0
        teacher_score_criteria_2 = row['Organisation'] if row['Organisation'] is not None else 0
        teacher_score_criteria_3 = row['Language'] if row['Language'] is not None else 0
        update_evaluation_data(
            evaluation_data, criteria_0, "Profesor", teacher_score_criteria_0)
        update_evaluation_data(
            evaluation_data, criteria_1, "Profesor", teacher_score_criteria_1)
        update_evaluation_data(
            evaluation_data, criteria_2, "Profesor", teacher_score_criteria_2)

        update_evaluation_data(
            evaluation_data, criteria_3, "Profesor", teacher_score_criteria_3)

        for model in models:
            logging.info("Processing model %s", model["name"])

            result = await process_writing(model["model"], level, institution, task, task_value, task_answer)

            ai_criteria_0_score = get_criteria_score(criteria_0, result)
            ai_criteria_1_score = get_criteria_score(criteria_1, result)
            ai_criteria_2_score = get_criteria_score(criteria_2, result)
            ai_criteria_3_score = get_criteria_score(criteria_3, result)

            update_evaluation_data(
                evaluation_data, criteria_0, model["name"], ai_criteria_0_score)

            update_evaluation_data(
                evaluation_data, criteria_1, model["name"], ai_criteria_1_score)

            update_evaluation_data(
                evaluation_data, criteria_2, model["name"], ai_criteria_2_score)

            update_evaluation_data(
                evaluation_data, criteria_3, model["name"], ai_criteria_3_score)

    return evaluation_data


async def main():
    """Main function"""
    logging.info("Starting main function")

    models = [
        {"name": "GPT-41", "model": LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_41)},
        {"name": "GPT-4O", "model": LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_4O)},
        {"name": "LLAMA4", "model": LanguageModelFactory.create_model(
            provider=Provider.GROQ, deployment=Deployment.LLAMA4)},
        {"name": "GEMINI-2.5-FLASH", "model": LanguageModelFactory.create_model(
            provider=Provider.GOOGLE, deployment=Deployment.GEMINI_2_5_FLASH)}
    ]

    # read the csv file
    df = pd.read_csv("tools/db_data/annotated_data.csv", delimiter=",", dtype={
        'Content': 'Float64',
        'Communicative Achievement': 'Float64',
        'Organisation': 'Float64',
        'Language': 'Float64'
    })
    df.fillna({
        'Content': 0.0,
        'Communicative Achievement': 0.0,
        'Organisation': 0.0,
        'Language': 0.0
    }, inplace=True)

    # Inicializar diccionario para almacenar datos por criterio
    # evaluation_data = {}
    logging.info("Reading dataframe")
    # read each row of the dataframe
    evaluation_data = load_evaluation_data()

    transpose_evaluation_data(evaluation_data)
    evaluation_data = await process(df, evaluation_data, models)
    # save_evaluation_data(evaluation_data)
    # plot_comparison(evaluation_data)
    # plot_comparison_barras(evaluation_data)

    # mae_results = calculate_mae(evaluation_data)
    logging.info("\n--- MAE por criterio ---")
    # print_mae_results(mae_results)
    # print_mae_results_markdown(mae_results)


def get_criteria_score(criteria_name: str, result: WritingAIChainFeedback) -> int:
    """Get the score of a criteria from the result."""

    try:
        if result.criterias is None:
            return 0

        for criteria in result.criterias:
            if to_lower(criteria.criteria) == to_lower(criteria_name):
                return criteria.score if criteria.score is not None else 0
    except Exception as e:
        logging.error("Error getting criteria score: %s", e)
        return 0


def update_evaluation_data(evaluation_data, criteria, source, score):
    """Actualiza la estructura de datos de evaluación con nuevas puntuaciones."""
    if criteria not in evaluation_data:
        evaluation_data[criteria] = {}
    if source not in evaluation_data[criteria]:
        evaluation_data[criteria][source] = []
    evaluation_data[criteria][source].append(score)


def load_evaluation_data():
    """Load the evaluation data from a json file."""
    with open("tools/db_data/evaluation_data.json", "r") as f:
        return json.load(f)


def save_evaluation_data(evaluation_data):
    """Save the evaluation data to a json file."""
    with open("tools/db_data/evaluation_data.json", "w") as f:
        json.dump(evaluation_data, f)


def transpose_evaluation_data(evaluation_data):
    """Transpose the evaluation data."""
    rows = []

    # Procesar cada criterio (e.g., "Content", "Organisation", etc.)
    for criterion, evaluations in evaluation_data.items():
        # Determinar la cantidad de ejemplos
        num_items = len(next(iter(evaluations.values())))
        for i in range(num_items):
            row = {"Criterion": criterion}
            for model, scores in evaluations.items():
                row[model] = scores[i]
            rows.append(row)

    # Crear DataFrame
    df = pd.DataFrame(rows)

    # Reordenar columnas si se desea
    column_order = ["Criterion", "Profesor", "GPT-41",
                    "GPT-4O", "LLAMA4", "GEMINI-2.5-FLASH"]
    df = df[column_order]

    # Guardar a CSV
    df.to_csv("tools/db_data/evaluation_data_transposed.csv", index=False)


def plot_comparison(evaluation_data):
    """Visual comparison of Human vs Models per criterion (one plot per row)."""

    # save the evaluation data to a json file
    # save_evaluation_data(evaluation_data)

    criterios = list(evaluation_data.keys())
    num_criterios = len(criterios)

    # Gráfico vertical: una fila por criterio
    fig, axes = plt.subplots(num_criterios, 1, figsize=(
        14, 4 * num_criterios), sharex=False)

    # Añadir espacio entre subplots
    # Aumenta el espacio vertical entre subplots
    plt.subplots_adjust(hspace=0.4)
    if num_criterios == 1:
        axes = [axes]  # Asegura que sea iterable

    line_styles = {
        "Profesor": {"color": "black", "linestyle": "-", "marker": "o", "linewidth": 2.5},
        "GPT-41": {"color": "blue", "linestyle": "--", "marker": "s", "linewidth": 2},
        "GPT-4O": {"color": "green", "linestyle": "-.", "marker": "x", "linewidth": 2},
        "LLAMA4": {"color": "red", "linestyle": ":", "marker": "D", "linewidth": 2},
        "GEMINI-2.5-FLASH": {"color": "purple", "linestyle": "-", "marker": "P", "linewidth": 2}
    }

    for i, criterio in enumerate(criterios):
        ax = axes[i]
        data = evaluation_data[criterio]

        # Asegura que todos los modelos tengan la misma cantidad de datos
        max_len = min(len(s) for s in data.values())
        indices = [str(i) for i in range(max_len)]

        for source, scores in data.items():
            style = line_styles.get(source, {})
            ax.plot(indices, scores[:max_len],
                    label=source, alpha=0.85, **style)

        # Eje Y desde 0 hasta el máximo + 1
        all_scores = [s for v in data.values()
                      for s in v[:max_len] if s is not None]
        if all_scores:
            max_score = int(np.ceil(max(all_scores))) + 1
        else:
            max_score = 1  # Valor predeterminado si no hay puntuaciones válidas

        ax.set_ylim(0, max_score)
        ax.set_yticks(range(0, max_score + 1))

        ax.set_title(f'Score- {criterio}')
        ax.set_xlabel('Sample Index')
        ax.set_ylabel('Score')
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.legend(loc="upper right")

    # Título general
    fig.suptitle('Score per Sample Comparison by Criterion (Human vs Models)',
                 fontsize=16, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


def plot_comparison_barras(evaluation_data):
    """Plot the comparison between Profesor and models by criterion."""

    criterios = list(evaluation_data.keys())
    modelos = ["Profesor", "GPT-41", "GPT-4O", "LLAMA4", "GEMINI-2.5-FLASH"]
    x = np.arange(len(modelos))
    width = 0.2  # Ancho de cada barra

    num_criterios = len(criterios)
    _, axes = plt.subplots((num_criterios + 1) // 2,
                           2, figsize=(14, 5 * ((num_criterios + 1) // 2)))
    axes = axes.flatten()

    for i, criterio in enumerate(criterios):
        ax = axes[i]
        data = evaluation_data[criterio]
        valores_promedio = []
        for m in modelos:
            # Obtener la lista de puntuaciones y convertir None a np.nan
            scores = [s if s is not None else np.nan for s in data.get(m, [])]
            # Calcular la media ignorando np.nan
            mean_score = np.nanmean(scores) if scores else np.nan
            valores_promedio.append(mean_score)

        ax.bar(x, valores_promedio, width, tick_label=modelos,
               color=["black", "blue", "green", "red", "purple"])

        ax.set_title(f'Comparación promedio - {criterio}')
        ax.set_ylim(0, 6)
        ax.set_ylabel('Puntuación promedio')
        ax.grid(True, axis='y')

    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.show()


def get_indices(puntuaciones_profesor: list[int]) -> list[str]:
    """Get the indices of the puntuaciones_profesor."""
    return [f"{i}" for i in range(len(puntuaciones_profesor))]


def to_lower(text: str) -> str:
    """Convert a text to lowercase and remove spaces."""
    return text.lower().strip()


def print_mae_results(mae_results):
    """Print the MAE results."""
    modelos = ["GPT-41", "GPT-4O", "LLAMA4", "GEMINI-2.5-FLASH"]

    print("\n--- MAE por criterio ---")
    for criteria, model_maes in mae_results.items():
        print(f"\n{criteria}:")
        for model in modelos:
            mae = model_maes.get(model, "N/A")
            print(f"  {model}: MAE = {mae}")


def print_mae_results_markdown(mae_results):
    """Print the MAE results in a Markdown-formatted table."""
    modelos = ["GPT-41", "GPT-4O", "LLAMA4", "GEMINI-2.5-FLASH"]
    table = PrettyTable()

    # Define the column headers
    table.field_names = ["Criterion"] + modelos

    # Add rows to the table
    for criterion, model_maes in mae_results.items():
        row = [criterion]
        for model in modelos:
            mae = model_maes.get(model, "N/A")
            row.append(mae)
        table.add_row(row)

    # Print the table
    print(table)


def calculate_mae(evaluation_data):
    """Calcula el MAE entre cada modelo y el profesor por criterio."""
    maes = {}
    modelos = ["GPT-41", "GPT-4O", "LLAMA4", "GEMINI-2.5-FLASH"]

    for criteria, sources in evaluation_data.items():
        maes[criteria] = {}

        teacher_scores = np.array(sources.get("Profesor", []))

        for model_name in modelos:
            model_scores = np.array(sources.get(model_name, []))

            if len(model_scores) != len(teacher_scores):
                logging.warning("Length mismatch in '%s' for model '%s': "
                                "%d vs %d", criteria, model_name, len(model_scores), len(teacher_scores))
                # O podrías usar np.nan o "N/A"
                maes[criteria][model_name] = None
                continue

            mae = np.mean(np.abs(model_scores - teacher_scores))
            maes[criteria][model_name] = round(mae, 3)

    return maes


if __name__ == "__main__":

    asyncio.run(main())
