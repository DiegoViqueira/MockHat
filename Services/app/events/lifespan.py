"""Lifespan"""
import logging
import threading
import json

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings
from app.services.user_service import UserService
from app.queue.consumer import SQSConsumer
from app.enums.role import Role
from app.models.account import Account
from app.models.user import User
from app.models.writing import Writing
from app.models.student import Student
from app.models.subscription import Subscription
from app.models.products import Products
from app.models.payment_history import PaymentHistory
from app.models.classes import Class
from app.models.assessment import Assessment
from app.services.auth_service import AuthService

from app.loggers.loggers import set_logger
from app.models.account_invitations import AccountInvitation

# Configuración de logging
set_logger()

logging.warning("Settings: %s", json.dumps(settings.model_dump(
    should_mask_secrets=True), indent=4))
# Variable global para el consumidor SQS
SQS_CONSUMER = None
SQS_THREAD = None


db_client = AsyncIOMotorClient(settings.mongo.URL, tls=True,
                               tlsAllowInvalidCertificates=False)


async def init_db() -> None:
    """Initialize the database."""
    logging.warning("Initializing database [%s]", settings.mongo.URL)
    logging.warning("Database: %s", settings.mongo.DATABASE)
    try:
        await init_beanie(database=db_client[settings.mongo.DATABASE], document_models=[Account, User, Writing, Student, Subscription,
                                                                                        Products, PaymentHistory, Class, Assessment, AccountInvitation])
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Error initializing database: %s", e)


async def init_db_admin_user() -> None:
    """Initialize admin user."""
    try:

        admin_user = await User.find(User.email == settings.auth.ADMIN_EMAIL).first_or_none()
        if not admin_user:
            hashed_password = AuthService.pwd_context.hash(
                settings.auth.ADMIN_PASSWORD)
            new_user = User(email=settings.auth.ADMIN_EMAIL, name="Administrator",
                            first_name="Administrator",
                            last_name="Administrator",
                            verified=True,
                            hashed_password=hashed_password,
                            role=Role.OWNER, disabled=False)

            await UserService.create_user_and_account(new_user, "MOCKHAT")
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Error initializing admin user: %s", e)


def start_sqs_consumer():
    """Inicia el consumidor SQS en un hilo separado."""
    global SQS_CONSUMER  # pylint: disable=global-statement

    if not settings.sqs.QUEUE_URL:
        logging.warning(
            "SQS_QUEUE_URL no está configurado. No se iniciará el consumidor SQS.")
        return

    try:
        logging.info("Iniciando consumidor SQS en un hilo separado")
        logging.info("Cola SQS: %s", settings.sqs.QUEUE_URL)
        logging.info("Región AWS: %s", settings.aws.REGION)
        logging.info("Hilos de procesamiento: %s",
                     settings.app.PROCESSING_THREADS)

        # Crear instancia del consumidor SQS
        SQS_CONSUMER = SQSConsumer(
            queue_url=settings.sqs.QUEUE_URL,
            region_name=settings.aws.REGION,
            max_workers=settings.app.PROCESSING_THREADS,
            wait_time=settings.sqs.WAIT_TIME
        )

        # Iniciar el consumidor en un hilo separado
        global SQS_THREAD  # pylint: disable=global-statement
        SQS_THREAD = threading.Thread(
            target=SQS_CONSUMER.start, name="SQSConsumerThread")
        SQS_THREAD.daemon = True  # El hilo se cerrará cuando el programa principal termine
        SQS_THREAD.start()

        logging.info(
            "Consumidor SQS iniciado correctamente en un hilo separado")
    except Exception as e:  # pylint: disable=broad-except
        logging.error("Error al iniciar el consumidor SQS: %s", e)


def stop_sqs_consumer():
    """Detiene el consumidor SQS de forma segura."""

    if SQS_CONSUMER:
        try:
            logging.info("Deteniendo el consumidor SQS...")
            SQS_CONSUMER.stop()

            if SQS_THREAD and SQS_THREAD.is_alive():
                SQS_THREAD.join(timeout=5)

            logging.info("Consumidor SQS detenido correctamente")
        except Exception as e:  # pylint: disable=broad-except
            logging.error("Error al detener el consumidor SQS: %s", e)
