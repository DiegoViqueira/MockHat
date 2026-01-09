"""Queue Service"""
import json
import logging

import boto3


from app.models.assessment_queue_message import AssessmentQueueMessage
from app.core.settings import settings


class QueueService:
    """Service to send messages to the queue."""

    def __init__(self):
        self.sqs_client = boto3.client(
            'sqs', region_name=settings.aws.REGION)
        self.queue_url = settings.sqs.QUEUE_URL

    def send_assessment_message(self, assessment: AssessmentQueueMessage) -> bool:
        """Send a message to the queue.

        Returns True if the message was sent successfully, False otherwise.
        """
        logging.info("Sending message to queue: %s", self.queue_url)
        try:

            message_body = json.dumps(assessment.model_dump())
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=message_body,
                MessageGroupId=assessment.assessment_id,
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                logging.error("Error sending message to queue: %s", response)
                return False

            return True
        except Exception as e:
            logging.error("Error sending message to queue: %s", e)
            return False
