"""Agent Publisher"""

import logging
import mimetypes
import os
import tempfile

from fastapi import UploadFile, Depends
import gradio as gr
from starlette.datastructures import Headers

from app.enums.exam_type import ExamType
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask
from app.enums.writing_state import WritingState
from app.events.lifespan import init_db
from app.i18n.locales.translation_manager import TranslationManager
from app.models.writing import Writing
from app.models.assessment_queue_message import WritingQueueMessage
from app.services.image_service import ImageService
from app.services.image_storage_provider import ImageStorageProvider
from app.services.queue_service import QueueService
from app.events.lifespan import init_db

logging.basicConfig(level=logging.INFO)


async def publish_writing(writing_id: str, image: str):
    """Publica un writing en la cola de mensajes."""
    await init_db()

    translation_manager = TranslationManager(lang="es")
    # Obtener el nombre deTranslationManager
    filename = os.path.basename(image)

    # Determinar el MIME type basado en la extensión del archivoWritingTask
    content_type, _ = mimetypes.guess_type(filename)
    if content_type is None:
        # Si no se puede determinar, usar un tipo genérico
        content_type = "application/octet-stream"

    # Crear un objeto UploadFile directamente desde el archivo
    with open(image, "rb") as file_object:

        headers = Headers({"content-type": content_type})
        upload_file = UploadFile(
            filename=filename,
            file=file_object,
            headers=headers
        )

        new_writing = Writing(
            assessment_id=writing_id,
            account_id="ACCOUNT_ID",
            user_id="USER_ID",
            student_id="STUDENT_ID",
            level=Level.B1,
            institution=Institution.CAMBRIDGE,
            exam_type=ExamType.CEQ,
            task=WritingTask.EMAIL,
        )

        await new_writing.save()

        # Generar el nombre de archivo para el writing
        image_url = await ImageService.generate_filename_for_writing(
            account_id=new_writing.account_id,
            writing_id=new_writing.id,
            file=upload_file
        )

        if image_url is None:
            new_writing.writing_state = WritingState.ERROR
            new_writing.error_message = translation_manager.translate(
                "Error generating image URL")
            await new_writing.save()
            return

        new_writing.student_response_image_url = image_url
        await new_writing.save()

        logging.info("Image URL: %s", image_url)

        # Subir el archivo a la cola de mensajes
        uploaded = await ImageStorageProvider.upload(
            filname=image_url,
            file=upload_file
        )

        if not uploaded:
            new_writing.writing_state = WritingState.ERROR
            new_writing.error_message = translation_manager.translate(
                "Error uploading file")
            await new_writing.save()
            return

        await new_writing.save()

    # Enviar el mensaje a la cola
    queue_service = QueueService()
    sent = queue_service.send_writing_message(
        WritingQueueMessage(
            writing_id=writing_id,
        )
    )

    if not sent:
        new_writing.writing_state = WritingState.ERROR
        new_writing.error_message = translation_manager.translate(
            "Error sending message to queue")
        await new_writing.save()
        return

    logging.info("Writing message sent")


def create_gradio_app():
    """Crea y configura la aplicación Gradio."""

    with gr.Blocks() as app:
        gr.Markdown("# Agent Publisher")
        gr.Markdown("Simulador de agentes para publicar la cola de mensajes")

        with gr.Row():
            writing_id = gr.Textbox(
                label="ID del Writing",
                placeholder="Ingresa el ID del writing",
                value="123"
            )

        with gr.Row():
            # Primera columna
            with gr.Column():
                gr.Markdown("### Imagen Writing")
                image_input1 = gr.Image(
                    type="filepath", label="Carga una imagen", width=500, height=500)
                publish_btn1 = gr.Button("Publicar Writing")

        publish_btn1.click(
            fn=publish_writing,
            inputs=[writing_id, image_input1],
            outputs=None
        )

    return app


if __name__ == "__main__":
    app = create_gradio_app()
    app.launch()
