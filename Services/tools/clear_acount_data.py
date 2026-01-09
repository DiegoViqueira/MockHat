import argparse
import asyncio

from app.models.user import User
from app.models.writing import Writing
from app.models.classes import Class
from app.models.assessment import Assessment
from app.events.lifespan import init_db
from app.services.image_storage_provider import ImageStorageProvider


async def main(account_id: str):
    """ Main"""

    if account_id is None:
        raise ValueError("Account ID is required")

    await init_db()

    print(f"***Eliminando datos de la cuenta {account_id}***")

    print("***Eliminando documentos de la colección writings***")
    writings_count = await Writing.find({"account_id": account_id}).count()

    writings = await Writing.find({"account_id": account_id}).to_list()
    for writing in writings:
        for image_url in writing.student_response_image_urls:
            print(
                f"Eliminando imagen {image_url} de writing {writing.id}")
            # ImageStorageProvider.delete(image_url)
        await writing.delete()

    print(
        f"Se eliminaron {writings_count} documentos de la colección writings")

    print("***Eliminando documentos de la colección classes***")
    classes_count = await Class.find({"account_id": account_id}).count()
    await Class.find({"account_id": account_id}).delete()
    print(f"Se eliminaron {classes_count} documentos de la colección classes")

    print("***Eliminando documentos de la colección assessments***")
    assessments_count = await Assessment.find({"account_id": account_id}).count()
    assessments = await Assessment.find({"account_id": account_id}).to_list()
    for assessment in assessments:
        ImageStorageProvider.delete(assessment.image_url)
        await assessment.delete()
    print(
        f"Se eliminaron {assessments_count} documentos de la colección assessments")


def parse_args():
    """ Parse arguments"""
    parser = argparse.ArgumentParser(description='Limpiar datos de cuenta')
    parser.add_argument(
        '--id',
        type=str,
        help='ID de la cuenta a limpiar',
        required=True
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.id))
