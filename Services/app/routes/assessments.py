"""Assessments"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Form, File, UploadFile
from fastapi.params import Depends
from starlette.requests import Request
from pymongo.errors import DuplicateKeyError

from app.chains.image_transcriber_chian import ImageTranscriberChain
from app.enums.deployment import Deployment
from app.enums.provider import Provider
from app.enums.role import Role
from app.enums.writing_state import WritingState
from app.factories.language_model_factory import LanguageModelFactory
from app.factories.writing_transcribe_prompt_factory import WritingTranscribePromptFactory
from app.models.assessment import Assessment
from app.enums.assessment_state import AssessmentState
from app.enums.institution import Institution
from app.enums.exam_type import ExamType
from app.enums.level import Level
from app.models.classes import Class
from app.models.gramar import Grammar
from app.models.student import Student
from app.models.update_text_request import UpdateAssessmentTextRequest
from app.models.user import User
from app.models.writing import Writing
from app.models.writing import WritingDto
from app.enums.writing_task import WritingTask
from app.models.assessment_queue_message import AssessmentQueueMessage
from app.models.writing_ai_feedback import WritingAIFeedback
from app.services.account_transaction_quota_manager import AccountTransactionQuotaManager
from app.services.image_service import ImageService
from app.services.image_storage_provider import ImageStorageProvider
from app.services.queue_service import QueueService
from app.models.assessments_polling import AssessmentsPolling
from app.enums.plan import Plan

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post("", response_model=Assessment,
             responses={
                 201: {"description": "Assessment created successfully"},
                 400: {"description": "Classroom ID is required"},
                 401: {"description": "Not authenticated"},
                 500: {"description": "Internal Server Error"},
             })
async def create_assessment(
        request: Request,
        title: str = Form(...),
        class_id: str = Form(...),
        institution: Institution = Form(...),
        exam_type: ExamType = Form(...),
        level: Level = Form(...),
        task: WritingTask = Form(...),
        file: UploadFile = File(...),
        writing_transcribe_prompt_factory: WritingTranscribePromptFactory = Depends(WritingTranscribePromptFactory)):
    """Crear una nueva evaluación."""

    translator = ImageTranscriberChain(
        model=LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_41))

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")
    if not class_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Classroom ID is required")

    try:

        assessment = Assessment(user_id=str(user.id))
        assessment.title = title
        assessment.account_id = user.account_id
        assessment.class_id = class_id
        assessment.institution = institution
        assessment.exam_type = exam_type
        assessment.level = level
        assessment.task = task

        await assessment.create()

        file_bytes, mime_type = await ImageService.uploadfile_to_bytes(file)

        if file_bytes is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image")

        base_64_image = await ImageService.encode_to_base64(file_bytes, mime_type)

        prompt = writing_transcribe_prompt_factory.get(task)

        transcription, spent_tokens_question = await translator.transcribe(
            image_url=base_64_image, specific_prompt=prompt)

        if transcription is None:
            await assessment.delete()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image")

        assessment.image_text = transcription.text
        assessment.image_transcription_tokens_usage = spent_tokens_question

        await assessment.save()

        image_url = await ImageService.generate_filename_for_writing(
            account_id=user.account_id,
            writing_id=assessment.id,
            content_type=mime_type
        )

        result = await ImageStorageProvider.upload(image_url, file_bytes, mime_type)

        if not result:
            await assessment.delete()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading assessment image")

        assessment.image_url = image_url
        await assessment.save()

        assessment.image_url = await ImageStorageProvider.get_url(assessment.image_url)

        return assessment

    except DuplicateKeyError as e:
        raise HTTPException(
            status_code=400, detail="Assessment already exists"
        ) from e
    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error("Error creating assessment: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating assessment") from e


@router.patch("/{assessment_id}/text", response_model=Assessment, responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def update_assessment_text(request: Request, assessment_id: str, update_text_request: UpdateAssessmentTextRequest):
    """Update an assessment."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found")

    assessment.image_text = update_text_request.text
    await assessment.save()

    assessment.image_url = await ImageStorageProvider.get_url(assessment.image_url)

    return assessment


@router.get("/class/{class_id}", response_model=List[Assessment], responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def get_assessment_by_class(request: Request, class_id: str, image_storage_provider: ImageStorageProvider = Depends(ImageStorageProvider)):
    """Get an assessment by ID."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessments = await Assessment.find(Assessment.class_id == class_id, Assessment.account_id == user.account_id).to_list()

    for assessment in assessments:
        assessment.image_url = await image_storage_provider.get_url(assessment.image_url)

    return assessments


@router.put("/{assessment_id}/writing", response_model=Writing, responses={
    401: {"description": "Not authenticated"},
    403: {"description": "You are not allowed to create a writing for this assessment"},
    404: {"description": "Assessment not found"},
    400: {"description": "Assessment is not in the pending state | Student not found in classroom | Teacher not found in classroom"},
    500: {"description": "Internal Server Error"},
})
async def upload_writing(request: Request,
                         assessment_id: str,
                         student_id: str = Form(...),
                         files: List[UploadFile] = File(...)):
    """Upload a writing for an assessment."""

    user = request.state.user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id, Assessment.account_id == user.account_id)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    if assessment.account_id != user.account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to create a writing for this assessment")

    # if assessment.state != AssessmentState.PENDING:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Assessment is not in the pending state")

    classroom = await Class.find_one(Class.id == assessment.class_id)

    if student_id not in [student.id for student in classroom.students]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student not found in classroom")

    if user.role == Role.MEMBER:
        if user.id not in [teacher.id for teacher in classroom.teachers]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Teacher not found in classroom")

    writing_found = await Writing.find_one(Writing.assessment_id == assessment_id,
                                           Writing.student_id == student_id,
                                           Writing.account_id == user.account_id,
                                           Writing.class_id == assessment.class_id)

    if writing_found:
        writing = writing_found
    else:
        writing = Writing(assessment_id=assessment_id,
                          student_id=student_id,
                          account_id=assessment.account_id,
                          class_id=assessment.class_id,
                          user_id=user.id,
                          level=assessment.level,
                          institution=assessment.institution,
                          exam_type=assessment.exam_type,
                          task=assessment.task)

    await writing.save()

    for index, file in enumerate(files):

        file_bytes, mime_type = await ImageService.uploadfile_to_bytes(file)

        if file_bytes is None:
            await writing.delete()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image")

        image_url = await ImageService.generate_filename_for_writing(
            account_id=user.account_id,
            writing_id=writing.id,
            content_type=mime_type,
            index=index
        )

        writing.student_response_image_urls.append(image_url)

        result = await ImageStorageProvider.upload(image_url, file_bytes, mime_type)

        if not result:
            await writing.delete()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error uploading assessment image")

    await writing.save()

    writing.student_response_image_urls = [await ImageStorageProvider.get_url(image_url) for image_url in writing.student_response_image_urls]

    usage = await AccountTransactionQuotaManager.get_account_transaction_usage(user.account_id)

    if (usage > 50 and user.plan in [Plan.FREE, Plan.BASIC, Plan.PREMIUM]) or (usage > 1000 and user.plan in [Plan.BUSINESS]) or (usage > 2000 and user.plan in [Plan.BUSINESS_PRO]):
        writing.state = WritingState.ERROR
        writing.error_message = "Account transaction quota exceeded"
        await writing.save()

    return writing


@router.post("/{assessment_id}/start", response_model=Assessment, responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def start_grading_process(request: Request, assessment_id: str, queue_service: QueueService = Depends(QueueService)):
    """Start grading an assessment."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id, Assessment.account_id == user.account_id)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    # if assessment.state != AssessmentState.PENDING:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Assessment is not in the pending state")

    queued = queue_service.send_assessment_message(
        AssessmentQueueMessage(assessment_id=assessment_id))

    if not queued:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error sending assessment message to queue")

    assessment.state = AssessmentState.STARTED
    await assessment.save()

    assessment.image_url = await ImageStorageProvider.get_url(assessment.image_url)

    return assessment


@router.patch("/{assessment_id}/writing/{writing_id}/ai-feedback", response_model=WritingAIFeedback, responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def update_writing_ai_feedback(request: Request, assessment_id: str,  writing_id: str, ai_feedback: WritingAIFeedback):
    """Update a writing ai feedback."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    writing = await Writing.find_one(Writing.id == writing_id, Writing.assessment_id == assessment_id, Writing.account_id == user.account_id)

    if not writing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Writing not found")

    if len(ai_feedback.criterias) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Criteria is required")

    writing.ai_feedback = ai_feedback

    await writing.save()

    return writing.ai_feedback


@router.patch("/{assessment_id}/writing/{writing_id}/grammar", response_model=Grammar, responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def update_writing_grammar(request: Request, assessment_id: str,  writing_id: str, grammar: Grammar):
    """Update a writing grammar."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    writing = await Writing.find_one(Writing.id == writing_id, Writing.assessment_id == assessment_id, Writing.account_id == user.account_id)

    if not writing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Writing not found")

    writing.grammar_feedback = grammar
    await writing.save()

    return writing.grammar_feedback


@router.get("/{assessment_id}/writings", response_model=List[WritingDto], responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def get_writings(request: Request, assessment_id: str):
    """Get writings for an assessment."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id, Assessment.account_id == user.account_id)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    writings = await Writing.find(Writing.assessment_id == assessment_id, Writing.account_id == user.account_id).to_list()

    writing_dtos = []
    for writing in writings:
        student = await Student.find_one(Student.id == writing.student_id)
        user = await User.find_one(User.id == writing.user_id)
        writing_dto = WritingDto(
            id=writing.id,
            assessment_id=writing.assessment_id,
            class_id=writing.class_id,
            student=student,
            account_id=writing.account_id,
            user=user,
            level=writing.level,
            institution=writing.institution,
            exam_type=writing.exam_type,
            task=writing.task,
            student_response_image_urls=writing.student_response_image_urls,
            student_response_text=writing.student_response_text,
            student_response_word_count=writing.student_response_word_count,
            student_response_tokens_usage=writing.student_response_tokens_usage,
            grammar_feedback=writing.grammar_feedback,
            grammar_feedback_tokens_usage=writing.grammar_feedback_tokens_usage,
            ai_feedback=writing.ai_feedback,
            writing_state=writing.writing_state,
            error_message=writing.error_message,
            writing_score=writing.writing_score,
            created_at=writing.created_at,
            updated_at=writing.updated_at
        )

        # TODO: Add image urls SOMETHING BY PLAN FEATURES ??
        # writing_dto.student_response_image_urls = [await ImageStorageProvider.get_url(image_url) for image_url in writing.student_response_image_urls]

        writing_dtos.append(writing_dto)

    return writing_dtos


@router.get("/{assessment_id}", response_model=Assessment, responses={
    401: {"description": "Not authenticated"},
    404: {"description": "Assessment not found"},
    500: {"description": "Internal Server Error"},
})
async def get_assessment(request: Request, assessment_id: str):
    """Get an assessment by ID."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id, Assessment.account_id == user.account_id)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found")

    assessment.image_url = await ImageStorageProvider.get_url(assessment.image_url)

    return assessment


@router.get("/pooling/started", response_model=AssessmentsPolling, responses={
    401: {"description": "Not authenticated"},
    500: {"description": "Internal Server Error"},
})
async def pooling_assessments_started(request: Request):
    """Get assessments started."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessments = await Assessment.find(Assessment.account_id == user.account_id, Assessment.state == AssessmentState.STARTED).to_list()

    if not assessments:
        return AssessmentsPolling(count=0, assessments=[])

    return AssessmentsPolling(count=len(assessments), assessments=[assessment.id for assessment in assessments])


@router.get("/{assessment_id}/pooling/finished", response_model=Assessment, responses={
    401: {"description": "Not authenticated"},
    500: {"description": "Internal Server Error"},
})
async def get_assessment_finished(request: Request, assessment_id: str):
    """Get an assessment by ID."""

    user = request.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated")

    assessment = await Assessment.find_one(Assessment.id == assessment_id, Assessment.account_id == user.account_id)

    if not assessment:
        return None

    assessment.image_url = await ImageStorageProvider.get_url(assessment.image_url)

    return assessment
