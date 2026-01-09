import argparse
import asyncio
from typing import Optional

from app.enums.assessment_state import AssessmentState
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask
from app.events.lifespan import init_db
from app.factories.few_shot_factory import FewShotWritingFactory
from app.models.assessment import Assessment
from app.models.writing import Writing
from app.enums.writing_state import WritingState
from app.services.queue_service import QueueService
from app.models.assessment_queue_message import AssessmentQueueMessage


async def process_assessment(assessment_id: str):
    """Process a specific assessment"""
    # Tu lógica de procesamiento aquí

    queue_service = QueueService()

    assessment = await Assessment.find_one(Assessment.id == assessment_id)

    if assessment is None:
        print(f"Assessment not found: {assessment_id}")
        return

    writings = await Writing.find(Writing.assessment_id == assessment_id, Writing.writing_state == WritingState.ERROR).to_list()

    for writing in writings:
        print(f"Processing writing: {writing.id}")
        writing.writing_state = WritingState.PENDING
        await writing.save()

    queued = queue_service.send_assessment_message(
        AssessmentQueueMessage(assessment_id=assessment_id))

    assessment.state = AssessmentState.STARTED
    await assessment.save()
    if queued:
        print(f"Assessment queued: {assessment_id}")
    else:
        print(f"Assessment not queued: {assessment_id}")


async def few_shot_writing_db():
    """Process all assessments"""
    factory = FewShotWritingFactory()
    few_shot_writing = factory.get_few_shot_prompt(
        Institution.BACHILLERATO, Level.EBAU, WritingTask.FORMAL_APPLICATION_EMAIL)
    print(few_shot_writing)


async def main(assessment_id: Optional[str] = None):

    await init_db()
    """Main function"""
    if assessment_id:
        # Procesar un assessment específico
        await process_assessment(assessment_id)
        # await few_shot_writing_db()
    else:
        # Procesar todos los assessments (tu lógica actual)
        print("Processing all assessments")


def parse_args():
    parser = argparse.ArgumentParser(description='Reprocesar assessments')
    parser.add_argument(
        '--id',
        type=str,
        help='ID específico del assessment a procesar',
        required=False
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args.id))
