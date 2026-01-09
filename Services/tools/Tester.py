"""Tester"""
import re
import os
import tempfile
import asyncio
from typing import Dict, Any

import gradio as gr
from fastapi import UploadFile

from app.chains.grammar_correction_chain import GrammarCorrectionChain
from app.chains.writing_correction_chain import WritingCorrectionChain
from app.factories.rubric_factory import RubricFactory
from app.factories.few_shot_factory import FewShotWritingFactory
from app.factories.writing_transcribe_prompt_factory import WritingTranscribePromptFactory
from app.models.writing_ai_chain_feedback import WritingAIChainFeedback
from app.services.image_service import ImageService
from app.chains.image_transcriber_chian import ImageTranscriberChain
from app.enums.writing_task import WritingTask
from app.enums.institution import Institution
from app.enums.level import Level
from app.models.token_usage import TokensUsage
from app.factories.language_model_factory import LanguageModelFactory
from app.enums.deployment import Deployment
from app.enums.provider import Provider


class GradioImageTranscriber:
    """Clase para manejar la transcripción de imágenes con Gradio."""

    def __init__(self):
        """Inicializa los servicios necesarios."""
        self.image_service = ImageService()
        model = LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_4O)
        self.transcriber_chain = ImageTranscriberChain(model=model)

    async def process_image(self, image_path: str) -> Dict[str, Any]:
        """Procesa una imagen y devuelve su transcripción.

        Args:
            image_path: Ruta a la imagen a procesar

        Returns:
            Diccionario con la transcripción y estadísticas de uso de tokens
        """
        # Crear un UploadFile desde la ruta de la imagen
        with open(image_path, "rb") as f:
            file_content = f.read()

        # Crear un archivo temporal para simular un UploadFile
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(file_content)
        temp_file.close()

        # Crear un objeto UploadFile simulado
        filename = os.path.basename(image_path)
        upload_file = UploadFile(
            filename=filename,
            file=open(temp_file.name, "rb")
        )

        try:
            # Convertir la imagen a base64
            data_url = await self.image_service.file_to_data_url(upload_file)

            transcribe_prompt_factory = WritingTranscribePromptFactory()
            # Transcribir la imagen
            transcription, token_usage = await self.transcriber_chain.transcribe(data_url, transcribe_prompt_factory.get(WritingTask.EMAIL))

            return transcription.text, token_usage
        finally:
            # Cerrar y eliminar el archivo temporal
            upload_file.file.close()
            os.unlink(temp_file.name)

    def gradio_process_image(self, image_path: str) -> str:
        """Versión sincrónica para Gradio que procesa una imagen.

        Args:
            image_path: Ruta a la imagen a procesar

        Returns:
            Texto transcrito de la imagen
        """
        result = asyncio.run(self.process_image(image_path))

        return result


class ChainCorrector:
    """Clase para manejar la corrección de escrituras con Gradio."""

    def __init__(self):
        model = LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_4O)
        self.chain_corrector = WritingCorrectionChain(model=model)
        self.grammar_correction_chain = GrammarCorrectionChain(model=model)
        self.few_shot_writing_factory = FewShotWritingFactory()
        self.rubric_factory = RubricFactory()

    def process_writing(self, level: Level, institution: Institution, task: WritingTask, task_value: str, task_answer: str) -> str:
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

        institution_enum = Institution(institution)
        level_enum = Level(level)
        task_enum = WritingTask(task)

        rubric = self.rubric_factory.get_rubric(
            institution_enum, level_enum, task_enum)
        print(
            f"Processing writing for level: {level}, institution: {institution}, task: {task}")
        grammar_correction, grammar_correction_token_usage = self.process_grammar_correction(
            task_answer)
        examples = self.few_shot_writing_factory.get_few_shot_prompt(
            institution_enum, level_enum, task_enum)
        result, token_usage = asyncio.run(
            self.chain_corrector.run(level_enum, institution_enum, task_enum, rubric, grammar_correction.to_string(), task_value, task_answer, self.count_words(task_value), examples))

        return self.format_writing_feedback(result), token_usage, grammar_correction.to_string(), grammar_correction_token_usage, self.count_words(task_value)

    def count_words(self, text: str) -> int:
        """Count the number of words in a text, ignoring punctuation."""
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return len(cleaned_text.split())

    def process_grammar_correction(self, text: str) -> str:
        """Procesa una corrección de gramática y devuelve la corrección.

        Args:
            text: Texto a corregir
        """
        return asyncio.run(
            self.grammar_correction_chain.run(text))

    def format_writing_feedback(self, criterias: WritingAIChainFeedback):

        formatted_text = "# Evaluación de Escritura\n\n"

        for criteria in criterias.criterias:
            formatted_text += f"## {criteria.criteria} - Puntuación: {criteria.score}/5\n"
            formatted_text += f"{criteria.feedback}\n\n"

        return formatted_text


def create_gradio_app():
    """Crea y configura la aplicación Gradio."""
    transcriber = GradioImageTranscriber()
    chain_corrector = ChainCorrector()

    with gr.Blocks() as app:
        gr.Markdown("# Writing Corrector")
        gr.Markdown("Carga imágenes para transcribir su contenido a texto")

        with gr.Row():
            gr.Markdown("### Level Selection")
            level_dropdown = gr.Dropdown(
                choices=[level.value for level in Level], value=Level.B1.value)

            gr.Markdown("### Institution Selection")
            institution_dropdown = gr.Dropdown(
                choices=[institution.value for institution in Institution], value=Institution.CAMBRIDGE.value)

            gr.Markdown("### Task Selection")
            task_dropdown = gr.Dropdown(choices=[task.value for task in WritingTask],
                                        value=WritingTask.EMAIL.value)

        with gr.Row():
            # Primera columna
            with gr.Column():
                gr.Markdown("### Imagen Assessment")
                image_input1 = gr.Image(
                    type="filepath", label="Carga una imagen", width=500, height=500)
                transcribe_btn1 = gr.Button("Transcribir Imagen Assessment")
                output1 = gr.Textbox(
                    label="Resultado de la transcripción", lines=10)
                tokens_assessment_transcribe = gr.Textbox(
                    label="Tokens Usage", lines=10)

            # Segunda columna
            with gr.Column():
                gr.Markdown("### Imagen Task")
                image_input2 = gr.Image(
                    type="filepath", label="Carga una imagen", width=500, height=500)
                transcribe_btn2 = gr.Button("Transcribir Imagen Task")
                output3 = gr.Textbox(
                    label="Resultado de la transcripción", lines=10)
                tokens_task_transcribe = gr.Textbox(
                    label="Tokens Usage", lines=10)

        # Configurar eventos
        transcribe_btn1.click(
            fn=transcriber.gradio_process_image,
            inputs=image_input1,
            outputs=[output1, tokens_assessment_transcribe]
        )

        transcribe_btn2.click(
            fn=transcriber.gradio_process_image,
            inputs=image_input2,
            outputs=[output3, tokens_task_transcribe]
        )

        with gr.Row():
            chain_corrector_btn = gr.Button("Corregir")

        with gr.Row():
            with gr.Column():
                output9 = gr.Textbox(
                    label="Palabras de la respuesta", lines=10, max_lines=400)

            with gr.Column():
                output5 = gr.Textbox(
                    label="Resultado de la corrección", lines=10, max_lines=400)

            with gr.Column():
                tokens_correction = gr.Textbox(
                    label="Tokens Correction", lines=10, max_lines=400)

            with gr.Column():
                output7 = gr.Textbox(
                    label="Corrección de gramática", lines=10, max_lines=400)

            with gr.Column():
                tokens_grammar_correction = gr.Textbox(
                    label="Tokens Correction", lines=10, max_lines=400)

        chain_corrector_btn.click(
            fn=chain_corrector.process_writing,
            inputs=[level_dropdown, institution_dropdown,
                    task_dropdown, output1, output3],
            outputs=[output5, tokens_correction, output7,
                     tokens_grammar_correction, output9],

        )

        with gr.Row():
            gr.Markdown("### Tokens Usage")
            suma_tokens = gr.Textbox(
                label="Tokens Usage", lines=10, max_lines=400)

            btn_calculate_tokens_usage = gr.Button("Calculate Tokens Usage")

            btn_calculate_tokens_usage.click(
                fn=calculate_tokens_usage,
                inputs=[tokens_assessment_transcribe, tokens_task_transcribe,
                        tokens_correction, tokens_grammar_correction],
                outputs=suma_tokens
            )

    return app


def parse_token_usage_string(token_usage_str):
    token_dict = {}
    for pair in token_usage_str.split():
        key, value = pair.split('=')
        token_dict[key] = value
    return token_dict


def create_tokens_usage_instance(token_usage_str):
    token_dict = parse_token_usage_string(token_usage_str)
    tokens_usage = TokensUsage(
        prompt_tokens=int(token_dict.get('prompt_tokens', 0)),
        completion_tokens=int(token_dict.get('completion_tokens', 0)),
        total_tokens=int(token_dict.get('total_tokens', 0)),
        total_cost=float(token_dict.get('total_cost', 0.0)),
        cached_tokens=int(token_dict.get('cached_tokens', 0)),
        reasoning_tokens=int(token_dict.get('reasoning_tokens', 0))
    )
    return tokens_usage


def calculate_tokens_usage(tokens_assessment_transcribe: str, tokens_task_transcribe: str, tokens_correction: str, tokens_grammar_correction: str) -> TokensUsage:

    tokens_assessment_transcribe = create_tokens_usage_instance(
        tokens_assessment_transcribe)
    tokens_task_transcribe = create_tokens_usage_instance(
        tokens_task_transcribe)
    tokens_correction = create_tokens_usage_instance(tokens_correction)
    tokens_grammar_correction = create_tokens_usage_instance(
        tokens_grammar_correction)

    suma_tokens = TokensUsage(
        prompt_tokens=tokens_assessment_transcribe.prompt_tokens +
        tokens_task_transcribe.prompt_tokens +
        tokens_correction.prompt_tokens +
        tokens_grammar_correction.prompt_tokens,
        completion_tokens=tokens_assessment_transcribe.completion_tokens +
        tokens_task_transcribe.completion_tokens +
        tokens_correction.completion_tokens +
        tokens_grammar_correction.completion_tokens,
        total_tokens=tokens_assessment_transcribe.total_tokens +
        tokens_task_transcribe.total_tokens +
        tokens_correction.total_tokens +
        tokens_grammar_correction.total_tokens,
        total_cost=tokens_assessment_transcribe.total_cost +
        tokens_task_transcribe.total_cost +
        tokens_correction.total_cost +
        tokens_grammar_correction.total_cost,
        cached_tokens=tokens_assessment_transcribe.cached_tokens +
        tokens_task_transcribe.cached_tokens +
        tokens_correction.cached_tokens +
        tokens_grammar_correction.cached_tokens,
    )

    return suma_tokens


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
