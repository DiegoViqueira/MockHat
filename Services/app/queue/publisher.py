"""SQS Publisher"""
import json
import logging
import boto3

from app.core.settings import settings


class SQSPublisher:
    """SQS Publisher"""

    def __init__(self, queue_url: str = settings.sqs.QUEUE_URL, region_name: str = settings.aws.REGION):
        self.queue_url = queue_url
        self.sqs_client = boto3.client('sqs', region_name=region_name)

    def publish_message(self, message):
        """Publish a message to the SQS queue

        Args:
            message: Any object that can be serialized to JSON
        """

        try:
            # Serializar el mensaje a JSON
            message_body = json.dumps(message)
            self.sqs_client.send_message(
                QueueUrl=self.queue_url, MessageBody=message_body)
        except Exception as e:
            logging.error("Error al publicar mensaje en la cola: %s", e)
            raise e
