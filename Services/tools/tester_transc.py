"""Tester"""
import asyncio
from typing import Dict, Any

import difflib
from PIL import Image, ImageOps, ImageFilter
import pytesseract
import gradio as gr

from app.factories.writing_transcribe_prompt_factory import WritingTranscribePromptFactory
from app.services.image_service import ImageService
from app.chains.image_transcriber_chian import ImageTranscriberChain
from app.factories.language_model_factory import LanguageModelFactory
from app.enums.deployment import Deployment
from app.enums.provider import Provider


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class GradioImageTranscriber:
    """Clase para manejar la transcripción de imágenes con Gradio."""

    def __init__(self):
        """Inicializa los servicios necesarios."""
        self.image_service = ImageService()
        model = LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_4O, temperature=0.0, max_tokens=4000)
        self.transcriber_chain = ImageTranscriberChain(model=model)
        self.factory = WritingTranscribePromptFactory()

    def transcribir_imagen_con_tesseract(self, ruta_imagen: str) -> str:
        """
        Extrae texto exacto de una imagen usando Tesseract OCR.

        :param ruta_imagen: Ruta al archivo de imagen.
        :return: Texto extraído.
            """
        imagen = Image.open(ruta_imagen).convert("L")  # Escala de grises
        # Invertir si es necesario (blanco sobre negro)
        imagen = ImageOps.invert(imagen)
        imagen = imagen.point(lambda x: 0 if x < 140 else 255)  # Binarización
        imagen = imagen.filter(ImageFilter.MedianFilter()
                               )      # Quitar ruido leve

        texto = pytesseract.image_to_string(imagen, lang='eng')
        return texto

    async def process_image(self, image_path: str) -> str:
        """Procesa una imagen y devuelve su transcripción.

        Args:
            image_path: Ruta a la imagen a procesar

        Returns:
            Diccionario con la transcripción y estadísticas de uso de tokens
        """
        # Crear un UploadFile desde la ruta de la imagen
        with open(image_path, "rb") as f:
            file_content = f.read()
        try:
            # Convertir la imagen a base64
            image_as_base64 = await self.image_service.encode_to_base64(
                file_content, "image/jpeg")

            # Transcribir la imagen
            transcription, token_usage = await self.transcriber_chain.transcribe(image_as_base64)

            return transcription.text
        finally:
            pass

    def gradio_process_image(self, image_path: str) -> str:
        """Versión sincrónica para Gradio que procesa una imagen.

        Args:
            image_path: Ruta a la imagen a procesar

        Returns:
            Texto transcrito de la imagen
        """
        result = asyncio.run(self.process_image(image_path))
        # result = self.transcribir_imagen_con_tesseract(image_path)
        return result


def resaltar_diferencias_inline(original, transcripto):
    """Resalta diferencias e incluye texto fantasma para palabras eliminadas. Retorna HTML y conteo."""
    original_words = original.split()
    transcripto_words = transcripto.split()

    matcher = difflib.SequenceMatcher(None, original_words, transcripto_words)
    resultado = []
    cambios = 0  # Contador de diferencias

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            resultado.extend(transcripto_words[j1:j2])
        elif tag == 'replace':
            # Palabras reemplazadas
            cambios += max(i2 - i1, j2 - j1)
            for palabra in original_words[i1:i2]:
                resultado.append(
                    f"<span style='opacity:0.5; text-decoration:line-through; color:#888;'>{palabra}</span>")
            for palabra in transcripto_words[j1:j2]:
                resultado.append(
                    f"<span style='background-color:#ffd6d6;'>{palabra}</span>")
        elif tag == 'insert':
            cambios += (j2 - j1)
            for palabra in transcripto_words[j1:j2]:
                resultado.append(
                    f"<span style='background-color:#d6f5d6;'>{palabra}</span>")
        elif tag == 'delete':
            cambios += (i2 - i1)
            for palabra in original_words[i1:i2]:
                resultado.append(
                    f"<span style='opacity:0.5; text-decoration:line-through; color:#888;'>{palabra}</span>")

    html_resultado = ' '.join(resultado)
    return html_resultado, cambios


def create_gradio_app():
    """Crea y configura la aplicación Gradio."""
    transcriber = GradioImageTranscriber()

    with gr.Blocks() as app:
        gr.Markdown("# Image Transcriber")
        gr.Markdown("Carga imágenes para transcribir su contenido a texto")
        texto_original = """Nowadays, a lot of people want to become famose, but there are good things and disadvantages, with the private life and money.
First of all, when someone starts showing its private life on social media for example, has to be very intelligent to show only a part of it, because the followers are going to ask for more, and maybe he or she lose a bit the private life. In the other hand, some people like showing its life, because someone can see its self in their.
The money is one of the things that people like the most, and famous people earn more money than someone who works in a “normal job”, because they have collaboretions with importants brands and they get free objects like make up or clothes, or even some restaurants invite them to eat there.
In my opinion being famous could be a bit difficult, but if you have a good organization it mayhap be fun.
To conclude, being famous has advantages and disadvantages it depend on how do you organize yourself.
"""

        with gr.Row():
            # Primera columna
            with gr.Column():
                gr.Markdown("### Imagen")
                image_input1 = gr.Image(
                    type="filepath", label="Carga una imagen", width=500, height=500)
                transcribe_btn1 = gr.Button("Transcribir Imagen")

            with gr.Column():
                gr.Markdown("### Texto Original")
                gr.Textbox(value=texto_original,
                           label="Texto Original", lines=20)

            with gr.Column():
                gr.Markdown("### Texto Transcribido")
                output1 = gr.Textbox(
                    label="Resultado de la transcripción", lines=20)

                diff_count = gr.Textbox(
                    label="Número de diferencias", interactive=False)

        with gr.Row():
            diff_html = gr.HTML(label="Diferencias resaltadas")

        with gr.Row():
            diff_count = gr.Textbox(
                label="Número de diferencias", interactive=False)

        def procesar_y_comparar(imagen):
            transcripto = transcriber.gradio_process_image(imagen)
            html_resultado, cambios = resaltar_diferencias_inline(
                texto_original, transcripto)
            html_final = f"<div style='overflow:auto; white-space:pre-wrap; font-family:monospace;'>{html_resultado}</div>"
            return transcripto, html_final, str(cambios)

        # Configurar eventos
        transcribe_btn1.click(
            fn=procesar_y_comparar,
            inputs=image_input1,
            outputs=[output1, diff_html, diff_count]
        )

    return app


# Punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
