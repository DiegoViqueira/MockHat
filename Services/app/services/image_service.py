"""Image Service"""
import base64
from datetime import UTC, datetime
import logging
from mimetypes import guess_type
import mimetypes
from fastapi import UploadFile


class ImageService:
    """Servicio para gestionar imágenes."""

    @staticmethod
    async def encode_to_base64(file_bytes: bytes, mime_type: str):
        """Convert a local file to a Base64 string."""

        base64_encoded_data = base64.b64encode(file_bytes).decode('utf-8')

        return f"data:{mime_type};base64,{base64_encoded_data}"

    @staticmethod
    async def uploadfile_to_bytes(file: UploadFile) -> tuple[bytes, str]:
        """Convert a UploadFile to a bytes object."""
        # Guess the MIME  type of the file based on its filename
        mime_type, _ = guess_type(file.filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Default MIME type if none is found

        # Read the file content as bytes
        file_content = await file.read()
        # Restablecer el puntero al inicio del archivo
        await file.seek(0)

        return file_content, mime_type

    @staticmethod
    async def file_to_data_url(file: UploadFile):
        """Convert a local file to a data URL."""
        # Guess the MIME  type of the file based on its filename
        mime_type, _ = guess_type(file.filename)
        if mime_type is None:
            mime_type = 'application/octet-stream'  # Default MIME type if none is found

        # Read the file content as bytes
        file_content = await file.read()
        # Restablecer el puntero al inicio del archivo
        await file.seek(0)

        # Convert the file content to Base64
        base64_encoded_data = base64.b64encode(file_content).decode('utf-8')

        # Construct and return the data URL
        return f"data:{mime_type};base64,{base64_encoded_data}"

    @staticmethod
    async def generate_filename_for_writing(account_id: str, writing_id: str, content_type: str, index: str | None = None) -> str | None:
        """Generate a filename for writing to the database.

        Returns None if the file is not an image.
        Returns filename  with the following format {YEAR}/{MONTH}/{account_id}_{writing_id}{extention}
        """

        extention = mimetypes.guess_extension(content_type)
        if extention is None:
            return None
        # Read the file content as bytes
        year = datetime.now(UTC).year
        month = datetime.now(UTC).month

        if index is not None:
            return f"{year}/{month}/{account_id}_{writing_id}-{index}{extention}"
        return f"{year}/{month}/{account_id}_{writing_id}{extention}"
