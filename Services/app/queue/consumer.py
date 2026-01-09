"""SQS Consumer"""
import asyncio
import json
import queue
import threading
import time
import logging
from concurrent.futures import ThreadPoolExecutor

import boto3
from botocore.exceptions import ClientError

from app.core.settings import settings
from app.models.assessment_queue_message import AssessmentQueueMessage
from app.services.agent_service import AgentService


class SQSConsumer:
    """SQS Consumer"""

    def __init__(self, queue_url: str = settings.sqs.QUEUE_URL, region_name: str = settings.aws.REGION, max_workers: int = 5,
                 wait_time: int = 20):
        """
        Inicializa el consumidor de SQS.

        Args:
            queue_url (str): URL de la cola SQS
            region_name (str): Región de AWS
            max_workers (int): Número máximo de hilos trabajadores
            wait_time (int): Tiempo de espera para long polling en segundos
        """
        self.queue_url = queue_url
        self.sqs_client = boto3.client('sqs', region_name=region_name)
        self.max_workers = max_workers
        self.wait_time = wait_time
        self.shutdown_flag = threading.Event()
        self.receiver_thread = None
        self.executor = None
        self.message_queue = queue.Queue()
        self.agent_service = AgentService()
        self.loop = asyncio.get_event_loop()

    def start(self):
        """Inicia el consumidor con hilos para recibir y procesar mensajes."""
        logging.info("Iniciando consumidor SQS con %s hilos",
                     self.max_workers)

        # Hilo para recibir mensajes
        self.receiver_thread = threading.Thread(
            target=self._receive_messages_loop,
            name="ReceiverThread"
        )
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

        # Pool de hilos para procesar mensajes
        with ThreadPoolExecutor(max_workers=self.max_workers,
                                thread_name_prefix="Worker") as self.executor:
            while not self.shutdown_flag.is_set():
                try:
                    # Obtener mensaje de la cola interna con timeout
                    message = self.message_queue.get(timeout=1)
                    self.executor.submit(self._process_message, message)
                except queue.Empty:
                    continue
                except KeyboardInterrupt:
                    logging.info("Interrupción de teclado detectada")
                    self.stop()
                except (ConnectionError, TimeoutError, IOError) as e:
                    logging.error(
                        "Error inesperado al recibir mensajes: %s", e)
                    time.sleep(5)
                except Exception as e:  # pylint: disable=broad-except
                    logging.error(
                        "Error inesperado al recibir mensajes: %s", e)
                    time.sleep(5)

    def _receive_messages_loop(self):
        """Bucle continuo para recibir mensajes de SQS y ponerlos en la cola interna."""
        logging.info("Iniciando bucle de recepción de mensajes")

        while not self.shutdown_flag.is_set():
            try:
                response = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=10,  # Solicitar hasta 10 mensajes a la vez
                    WaitTimeSeconds=self.wait_time,  # Long polling
                    AttributeNames=['All'],
                    MessageAttributeNames=['All'],
                    # Para colas FIFO, puedes especificar el grupo de mensajes
                    # ReceiveRequestAttemptId=str(uuid.uuid4())  # Opcional para colas FIFO
                )

                messages = response.get('Messages', [])
                if messages:
                    logging.info("Recibidos %d mensajes", len(messages))
                    for message in messages:
                        self.message_queue.put(message)
            except ClientError as e:
                logging.error("Error al recibir mensajes de SQS: %s", e)
                time.sleep(5)  # Esperar antes de reintentar
            except Exception as e:  # pylint: disable=broad-except
                logging.error(
                    "Error inesperado al recibir mensajes: %s", e)
                time.sleep(5)

    def _process_message(self, message):
        """
        Procesa un mensaje individual de SQS.

        Args:
            message (dict): Mensaje de SQS
        """
        message_id = message['MessageId']
        receipt_handle = message['ReceiptHandle']

        try:
            logging.info("Procesando mensaje: %s", message_id)

            # Extraer el cuerpo del mensaje
            body = message['Body']

            # Intentar parsear como JSON si es posible
            try:
                body_json = json.loads(body)
            except json.JSONDecodeError:
                logging.info("Contenido del mensaje (texto): %s", body)

            # Aquí iría la lógica de procesamiento real del mensaje
            # Por ejemplo, guardar en base de datos, llamar a una API, etc.
            message_body = AssessmentQueueMessage(**body_json)

            future = asyncio.run_coroutine_threadsafe(
                self.agent_service.process_queue_message(
                    message_body), self.loop
            )

            future.result()
            logging.info(
                "Mensaje %s procesado y eliminado de la cola", message_id)

            self.sqs_client.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )

        except Exception as e:  # pylint: disable=broad-except
            logging.error(
                "Error al procesar mensaje %s: %s", message_id, e)

    def stop(self):
        """Detiene el consumidor de forma segura."""
        logging.info("Deteniendo el consumidor SQS...")
        self.shutdown_flag.set()
        if hasattr(self, 'receiver_thread') and self.receiver_thread.is_alive():
            self.receiver_thread.join(timeout=5)
        logging.info("Consumidor SQS detenido")
