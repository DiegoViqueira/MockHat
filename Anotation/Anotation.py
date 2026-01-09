import gradio as gr
import pandas as pd

# Variable global para almacenar el DataFrame y el índice actual
df = pd.DataFrame()
current_index = 0


def load_file(file):
    global df, current_index
    current_index = 0  # Reiniciar el índice al cargar un nuevo archivo
    df = pd.read_csv(file.name, delimiter=",", dtype={
        'Criteria 0 Teacher Score': 'Int64',
        'Criteria 1 Teacher Score': 'Int64',
        'Criteria 2 Teacher Score': 'Int64',
        'Criteria 3 Teacher Score': 'Int64'
    })
    df.fillna({
        'Criteria 0 Teacher Score': 0,
        'Criteria 1 Teacher Score': 0,
        'Criteria 2 Teacher Score': 0,
        'Criteria 3 Teacher Score': 0
    }, inplace=True)
    return next()


def update_df(teacher_score_0=None, teacher_score_1=None, teacher_score_2=None, teacher_score_3=None):

    global current_index, df
    if df.empty:
        return "No hay datos cargados.", "No hay datos cargados.", "", "", "", "", 0, 0, 0, 0, 0, 0, 0, 0

    # Guardar las puntuaciones del profesor ingresadas por el usuario
    if teacher_score_0 is not None:
        df.at[current_index, 'Criteria 0 Teacher Score'] = teacher_score_0
    if teacher_score_1 is not None:
        df.at[current_index, 'Criteria 1 Teacher Score'] = teacher_score_1
    if teacher_score_2 is not None:
        df.at[current_index, 'Criteria 2 Teacher Score'] = teacher_score_2
    if teacher_score_3 is not None:
        df.at[current_index, 'Criteria 3 Teacher Score'] = teacher_score_3


def next():
    global current_index, df
    if df.empty:
        return "No hay datos cargados.", "No hay datos cargados.", "", "", "", "", 0, 0, 0, 0, 0, 0, 0, 0

    if current_index >= len(df):
        current_index = 0  # Reiniciar al inicio si se supera el número de filas

    task = df.iloc[current_index]['Task']
    level = df.iloc[current_index]['Level']
    institution = df.iloc[current_index]['Institution']

    student_text = df.iloc[current_index]['text_response']
    teacher_text = df.iloc[current_index]['text_question']
    student_text = student_text.replace("\\n", "\n") if isinstance(
        student_text, str) else student_text
    teacher_text = teacher_text.replace("\\n", "\n") if isinstance(
        teacher_text, str) else teacher_text

    criteria_0 = df.iloc[current_index]['Criteria 0']
    criteria_1 = df.iloc[current_index]['Criteria 1']
    criteria_2 = df.iloc[current_index]['Criteria 2']
    criteria_3 = df.iloc[current_index]['Criteria 3']
    teacher_criteria_score_0 = df.iloc[current_index]['Criteria 0 Teacher Score']
    teacher_criteria_score_1 = df.iloc[current_index]['Criteria 1 Teacher Score']
    teacher_criteria_score_2 = df.iloc[current_index]['Criteria 2 Teacher Score']
    teacher_criteria_score_3 = df.iloc[current_index]['Criteria 3 Teacher Score']

    return (student_text, teacher_text, criteria_0, criteria_1, criteria_2, criteria_3,
            teacher_criteria_score_0, teacher_criteria_score_1, teacher_criteria_score_2, teacher_criteria_score_3, task, level, institution)


def next_row():
    global current_index
    current_index += 1
    return next()


def save_to_csv():
    global df
    df.to_csv("updated_scores.csv", index=False)
    return "Puntuaciones guardadas en 'updated_scores.csv'."


with gr.Blocks(css=".textbox {white-space: pre-wrap;}") as demo:
    with gr.Row():
        file_input = gr.File(label="Carga tu archivo CSV", file_types=[".csv"])
    with gr.Row():
        with gr.Column():
            teacher_text = gr.Textbox(
                label="Examen", lines=10, max_lines=100, interactive=False, elem_classes="textbox")
        with gr.Column():
            student_text = gr.Textbox(
                label="Respuesta del Alumno", lines=10, max_lines=100, interactive=False, elem_classes="textbox")
    with gr.Row():
        with gr.Column():
            task_text = gr.Textbox(label="Tarea", lines=1, interactive=False)
            level_text = gr.Textbox(label="Nivel", lines=1, interactive=False)
            institution_text = gr.Textbox(
                label="Institución", lines=1, interactive=False)

    with gr.Row():
        with gr.Column():
            criteria_0 = gr.Textbox(
                label="Criterio 0", lines=1, interactive=False)
            criteria_1 = gr.Textbox(
                label="Criterio 1", lines=1, interactive=False)
            criteria_2 = gr.Textbox(
                label="Criterio 2", lines=1, interactive=False)
            criteria_3 = gr.Textbox(
                label="Criterio 3", lines=1, interactive=False)
        with gr.Column():
            teacher_criteria_score_0 = gr.Number(
                label="Teacher Score 0", precision=0, interactive=True)
            teacher_criteria_score_1 = gr.Number(
                label="Teacher Score 1", precision=0, interactive=True)
            teacher_criteria_score_2 = gr.Number(
                label="Teacher Score 2", precision=0, interactive=True)
            teacher_criteria_score_3 = gr.Number(
                label="Teacher Score 3", precision=0, interactive=True)
    with gr.Row():
        next_button = gr.Button("Siguiente")
        save_button = gr.Button("Guardar Cambios")
        download_button = gr.Button("Exportar a CSV")

    file_input.upload(load_file, inputs=file_input,
                      outputs=[student_text, teacher_text, criteria_0, criteria_1, criteria_2, criteria_3,
                               teacher_criteria_score_0, teacher_criteria_score_1, teacher_criteria_score_2, teacher_criteria_score_3, task_text, level_text, institution_text])
    next_button.click(next_row,
                      outputs=[student_text, teacher_text, criteria_0, criteria_1, criteria_2, criteria_3,
                               teacher_criteria_score_0, teacher_criteria_score_1, teacher_criteria_score_2, teacher_criteria_score_3, task_text, level_text, institution_text,])

    save_button.click(update_df, inputs=[
                      teacher_criteria_score_0, teacher_criteria_score_1, teacher_criteria_score_2, teacher_criteria_score_3])

    download_button.click(save_to_csv)

# Ejecutar la aplicación
if __name__ == "__main__":
    demo.launch(show_api=False)
