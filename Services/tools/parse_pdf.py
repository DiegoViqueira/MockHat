
import gradio as gr
from llama_index.readers.file import PDFReader


def create_gradio_app():
    """Crea y configura la aplicación Gradio."""
    with gr.Blocks() as app:
        gr.Markdown("# PDF Parser")
        gr.Markdown("Carga un PDF para extraer su contenido")

        with gr.Row():
            with gr.Column():
                gr.Markdown("### PDF")
                pdf_input = gr.File(label="Carga un PDF")
                parse_btn = gr.Button("Parsear PDF")

            with gr.Column():
                gr.Markdown("### Contenido")
                content_output = gr.Textbox(
                    label="Contenido del PDF", interactive=False, lines=2000)

        def parse_pdf(pdf_file):
            """Función para extraer el contenido de un PDF."""
            # Aquí puedes implementar la lógica para extraer el contenido del PDF
            # Por ahora, solo devolvemos un mensaje de ejemplo
            reader = PDFReader()
            documents = reader.load_data(file=pdf_file)

            text = ""
            for document in documents:
                text += document.text

            return text

        parse_btn.click(parse_pdf, inputs=pdf_input,
                        outputs=content_output)

    return app


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
