"""Image Storage Provider"""
import base64
import logging
from io import BytesIO
import mimetypes
import boto3

from app.core.settings import settings

IMAGE_CONTENT_TYPE = 'image/jpeg'


class ImageStorageProvider:
    """Proveedor de almacenamiento de imágenes."""

    @staticmethod
    async def upload(filename: str, file_bytes: bytes, content_type: str) -> bool:
        """Upload an image file to S3. Returns True if successful."""
        try:
            # ⚠️ Verificar que el archivo no está vacío
            if not file_bytes:
                logging.error("Error: El archivo está vacío, no se subirá.")
                return False

            # ⚠️ Verificar el Content-Type
            if content_type not in ["image/jpeg", "image/png", "image/webp"]:
                logging.warning(
                    "Tipo de archivo desconocido, usando 'application/octet-stream'")
                content_type = "application/octet-stream"

            logging.info("Uploading %s to S3 with Content-Type: %s",
                         filename, content_type)

            # Subir a S3
            ImageStorageProvider._save_to_s3(
                filename,
                file_bytes,
                content_type
            )

            return True
        except Exception as e:
            logging.error("Error uploading file: %s", e)
            return False

    @staticmethod
    async def get_url(filname: str):
        """Get the image URL."""
        return await ImageStorageProvider._get_s3_url(filname)

    @staticmethod
    async def _get_s3_url(file_name: str, expires_in: int = 3600):
        """Get the S3 image URL."""
        client = boto3.client('s3')

        url = client.generate_presigned_url('get_object',
                                            Params={'Bucket': f"{settings.s3.BUCKET_NAME}",
                                                    'Key': file_name},
                                            ExpiresIn=expires_in
                                            )

        return url

    @staticmethod
    def get_s3_image_as_base64(file_name: str):
        """Fetch image from S3 and return as Base64 data URL."""
        s3 = boto3.client('s3')

        # Get the object from S3
        response = s3.get_object(
            Bucket=settings.s3.BUCKET_NAME, Key=file_name)
        file_content = response['Body'].read()

        # Guess MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(file_name)
        if not mime_type:
            mime_type = 'application/octet-stream'  # Fallback

        # Convert to Base64
        base64_encoded_data = base64.b64encode(file_content).decode('utf-8')

        # Return data URL
        return f"data:{mime_type};base64,{base64_encoded_data}"

    @staticmethod
    def _save_to_s3(file_name: str,
                    image_bytes: bytes,
                    content_type: str = IMAGE_CONTENT_TYPE
                    ):
        """Save the image to S3."""

        logging.info("Saving %s to S3 with Content-Type: %s",
                     file_name, content_type)
        s3_client = boto3.client('s3')

        bucket_name = f"{settings.s3.BUCKET_NAME}"

        file_like_object = BytesIO(image_bytes)
        s3_client.upload_fileobj(Fileobj=file_like_object,
                                 Bucket=bucket_name,
                                 Key=file_name,
                                 ExtraArgs={'ContentType': content_type})

    @staticmethod
    def delete(file_name: str):
        """Delete the image from S3."""
        ImageStorageProvider._delete_from_s3(file_name)

    @staticmethod
    def _delete_from_s3(file_name: str):
        """Delete the image from S3."""
        s3_client = boto3.client('s3')
        s3_client.delete_object(
            Bucket=settings.s3.BUCKET_NAME, Key=file_name)
