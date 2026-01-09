"""Agent service"""
import logging
import re
from typing import List

from app.chains.grammar_correction_chain import GrammarCorrectionChain
from app.chains.image_transcriber_chian import ImageTranscriberChain
from app.chains.writing_correction_chain import WritingCorrectionChain
from app.decorators.benchmark import benchmark
from app.enums.assessment_state import AssessmentState
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.provider import Provider
from app.enums.writing_state import WritingState
from app.enums.deployment import Deployment
from app.factories.few_shot_factory import FewShotWritingFactory
from app.factories.grammar_prompt_factory import GrammarExtraPromptFactory
from app.factories.grammar_reference_factory import GrammarReferenceFactory
from app.factories.rubric_factory import RubricFactory
from app.factories.language_model_factory import LanguageModelFactory
from app.models.assessment import Assessment
from app.models.assessment_queue_message import AssessmentQueueMessage
from app.models.writing import Writing
from app.models.writing_ai_feedback import WritingAIFeedback
from app.services.image_storage_provider import ImageStorageProvider
from app.services.mail_service import MailService
from app.services.user_service import UserService
from app.errors.content_filter_error import ContentFilterError
from app.errors.lenght_reason_error import LenghtReasonError


class AgentService:
    """
    Service for managing agents.
    """

    def __init__(self):
        self.model = LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_41)
        self.model_2 = LanguageModelFactory.create_model(
            provider=Provider.AZURE, deployment=Deployment.GPT_41)
        self.model_alternative = LanguageModelFactory.create_model(
            provider=Provider.GROQ, deployment=Deployment.LLAMA4)
        self.transcriber_chain = ImageTranscriberChain(
            model=self.model_2)
        self.transcriber_chain_alternative = ImageTranscriberChain(
            model=self.model_alternative)
        self.grammar_correction_chain = GrammarCorrectionChain(
            model=self.model)
        self.writing_correction_chain = WritingCorrectionChain(
            model=self.model)
        self.grammar_correction_chain_alternative = GrammarCorrectionChain(
            model=self.model_alternative)
        self.writing_correction_chain_alternative = WritingCorrectionChain(
            model=self.model_alternative)

        self.rubric_factory = RubricFactory()
        self.few_shot_writing_factory = FewShotWritingFactory()
        self.grammar_extra_prompt_factory = GrammarExtraPromptFactory()
        self.grammar_reference_factory = GrammarReferenceFactory()

    async def process_queue_message(self, message: AssessmentQueueMessage):
        """
        Process a queue message.
        """

        try:
            assessment = await self._fetch_assessment(message.assessment_id)

            if assessment is not None:
                writings = await self._fetch_pending_writings(message.assessment_id)

                for writing in writings:
                    await self.process_writing(assessment.image_text, writing)

                await self._complete_assessment(assessment)

                return True
            else:
                logging.error(
                    "Assessment %s not found", message.assessment_id)
                return False

        except Exception as e:
            logging.error(
                "Error processing queue message %s: %s", message.assessment_id, str(e))
            return False

    async def process_writing(self, assessment_text: str, writing: Writing):
        """
        Process a single writing.
        """
        try:

            if writing.writing_state == WritingState.COMPLETED:
                return

            if writing.writing_state == WritingState.ERROR:
                logging.error(
                    "Writing %s is in error state with message %s", writing.id, writing.error_message)
                return

            if len(writing.student_response_image_urls) == 0:
                raise RuntimeError("No image URLs found")

            data_urls = []

            for image_url in writing.student_response_image_urls:
                data_urls.append(self._fetch_image_as_base64(image_url))

            transcription, token_usage = await self._transcribe_image(data_urls)

            if transcription is None:
                raise RuntimeError("Transcription failed")

            await self._update_writing_with_transcription(writing, transcription, token_usage)

            rubric = self._generate_rubric(writing)

            if rubric is None:
                raise RuntimeError("Rubric generation failed")

            grammar_feedback, grammar_tokens = await self._generate_grammar_feedback(writing.student_response_text, writing.level, writing.institution)

            if grammar_feedback is None:
                raise RuntimeError("Grammar feedback generation failed")

            writing.grammar_feedback = grammar_feedback
            writing.grammar_feedback_tokens_usage = grammar_tokens

            examples = self._fetch_few_shot_examples(writing)

            ai_feedback, ai_tokens = await self._generate_ai_feedback(writing, rubric, grammar_feedback, assessment_text, examples)

            if ai_feedback is None:
                raise RuntimeError("AI feedback generation failed")

            writing.ai_feedback = WritingAIFeedback(
                criterias=ai_feedback.criterias, spent_tokens=ai_tokens)
            writing.writing_state = WritingState.COMPLETED
            writing.error_message = ""

            await writing.save()

        except RuntimeError as e:
            writing.writing_state = WritingState.ERROR
            writing.error_message = str(e)
            await writing.save()
            logging.error(
                "Error processing writing %s: %s", writing.id, str(e))
            return False

        except ContentFilterError as e:
            writing.writing_state = WritingState.ERROR
            writing.error_message = str(e)
            await writing.save()
            logging.error(
                "Error processing writing %s: %s", writing.id, str(e))
            return False

        except Exception as e:
            writing.writing_state = WritingState.ERROR
            writing.error_message = str(e)
            await writing.save()
            logging.error(
                "Error processing writing %s: %s", writing.id, str(e))
            return False

    async def _send_finished_assessment_email(self, assessment: Assessment):
        user = await UserService.get_user(assessment.user_id)
        if user is None:
            logging.error(
                "User %s not found", assessment.user_id)
            return

        mail_service = MailService()
        mail_service.send_finished_assessment_email(
            user.email, assessment.title)

    async def _fetch_assessment(self, assessment_id: str) -> Assessment:
        return await Assessment.find_one(Assessment.id == assessment_id)

    async def _fetch_pending_writings(self, assessment_id: str):
        return await Writing.find_many(Writing.assessment_id == assessment_id, Writing.writing_state == WritingState.PENDING).to_list()

    async def _complete_assessment(self, assessment: Assessment):

        previous_state = assessment.state

        assessment.state = AssessmentState.COMPLETED
        await assessment.save()

        if previous_state == AssessmentState.STARTED:
            await self._send_finished_assessment_email(assessment)

    def _fetch_image_as_base64(self, image_url: str) -> str:
        return ImageStorageProvider.get_s3_image_as_base64(image_url)

    @benchmark("Transcribing image")
    async def _transcribe_image(self, data_urls: List[str]):

        try:
            return await self.transcriber_chain.transcribe_multiple_images(data_urls)
        except (ContentFilterError, LenghtReasonError):
            return await self.transcriber_chain_alternative.transcribe_multiple_images(data_urls)
        except Exception as e:
            logging.error(
                "Error transcribing image: %s", str(e))
            raise e

    async def _update_writing_with_transcription(self, writing: Writing, transcription, token_usage: int):
        writing.student_response_text = transcription.text
        writing.student_response_tokens_usage = token_usage
        writing.student_response_word_count = self._count_words(
            transcription.text)
        await writing.save()

    def _generate_rubric(self, writing: Writing):
        return self.rubric_factory.get_rubric(writing.institution, writing.level, writing.task)

    @benchmark("Generating grammar feedback")
    async def _generate_grammar_feedback(self, text: str, level: Level, institution: Institution):

        try:
            grammar_reference = self.grammar_reference_factory.get_grammar_reference(
                institution, level)
            extra_prompt = self.grammar_extra_prompt_factory.get(level)
            return await self.grammar_correction_chain.run(text, extra_prompt, grammar_reference)
        except ContentFilterError as e:
            logging.error(
                "Content filter error generating grammar feedback: %s", str(e))
            return await self.grammar_correction_chain_alternative.run(text, extra_prompt, grammar_reference)
        except LenghtReasonError as e:
            logging.error(
                "Length reason error generating grammar feedback: %s", str(e))
            return await self.grammar_correction_chain_alternative.run(
                text, extra_prompt, grammar_reference)
        except Exception as e:
            logging.error(
                "Error generating grammar feedback: %s", str(e))
            raise e

    def _fetch_few_shot_examples(self, writing: Writing):
        return self.few_shot_writing_factory.get_few_shot_prompt(writing.institution, writing.level, writing.task)

    @benchmark("Generating AI feedback")
    async def _generate_ai_feedback(self, writing: Writing, rubric, grammar_feedback, assessment_text: str, examples):

        try:
            return await self.writing_correction_chain.run(
                writing.level, writing.institution, writing.task, rubric,
                grammar_feedback.to_string(), assessment_text, writing.student_response_text,
                writing.student_response_word_count, examples
            )
        except ContentFilterError as e:
            logging.error(
                "Content filter error generating AI feedback: %s", str(e))
            return await self.writing_correction_chain_alternative.run(
                writing.level, writing.institution, writing.task, rubric,
                grammar_feedback.to_string(), assessment_text, writing.student_response_text,
                writing.student_response_word_count, examples
            )
        except LenghtReasonError as e:
            logging.error(
                "Length reason error generating AI feedback: %s", str(e))
            return await self.writing_correction_chain_alternative.run(
                writing.level, writing.institution, writing.task, rubric,
                grammar_feedback.to_string(), assessment_text, writing.student_response_text,
                writing.student_response_word_count, examples
            )
        except Exception as e:
            logging.error(
                "Error generating AI feedback: %s", str(e))
            raise e

    def _count_words(self, text: str) -> int:
        """Count the number of words in a text, ignoring punctuation."""
        cleaned_text = re.sub(r'[^\w\s]', '', text)
        return len(cleaned_text.split())
