"""Image Transcriber Chain"""
import logging
from typing import List
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from langchain_community.callbacks.manager import get_openai_callback


from app.chains import IMAGE_TRANSCRIBER_PROMPT
from app.enums.deployment import Deployment
from app.errors.lenght_reason_error import LenghtReasonError
from app.factories.language_model_factory import ModelEngine
from app.models.transcribe_ai_response import TranscribeAiResponse
from app.models.token_usage import TokensUsage
from app.handlers.debug_messages_handler import DebugMessagesHandler
from app.errors.content_filter_error import ContentFilterError


class ImageTranscriberChain:
    """
    Translate the content of an image to text.
    """

    def __init__(self, model: ModelEngine):
        # Inicializar el modelo de lenguaje de Azure OpenAI
        self.model = model
        self.llm = model.model
        self.structured_llm = self.llm.with_structured_output(
            TranscribeAiResponse)
        self.parser = PydanticOutputParser(
            pydantic_object=TranscribeAiResponse)
        self.using_parser = model.deployment != Deployment.GPT_4O and model.deployment != Deployment.GPT_41
        self.format_prompt = HumanMessage(
            content=f"Parse as follows: {self.parser.get_format_instructions()}")
        self.chain = self._build_chain()
        self.chain = self.chain.with_config(callbacks=[DebugMessagesHandler()])

    def _build_chain(self):
        logging.info("Using model %s %s", self.model.provider,
                     self.model.deployment)
        messages = [
            IMAGE_TRANSCRIBER_PROMPT
        ]

        if self.using_parser:
            messages.append(self.format_prompt)

        chat_prompt = ChatPromptTemplate.from_messages(messages)

        if self.using_parser:
            logging.info("Using Parser")
            return chat_prompt | self.llm | self.parser
        else:
            logging.info("Using Structured Output")
            return chat_prompt | self.structured_llm

    async def transcribe_multiple_images(self, image_urls: List[str], specific_prompt: str = None) -> tuple[TranscribeAiResponse, TokensUsage]:
        """
        Transcribe the content of an image to text.
        Returns:
            tuple: (TranscribeAiResponse, token_usage_dict)
        """

        aggregated_result = TranscribeAiResponse(text="")
        aggregated_tokens = TokensUsage(
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            total_cost=0,
            cached_tokens=0,
            reasoning_tokens=0
        )

        try:

            for image_url in image_urls:

                result, token_usage = await self.transcribe(
                    image_url, specific_prompt)

                if result is None:
                    logging.error(
                        "Failed to transcribe image: [ %s ]", image_url[:20])
                    return None, None

                aggregated_result.text += result.text
                aggregated_tokens.prompt_tokens += token_usage.prompt_tokens
                aggregated_tokens.completion_tokens += token_usage.completion_tokens
                aggregated_tokens.total_tokens += token_usage.total_tokens
                aggregated_tokens.total_cost += token_usage.total_cost
                aggregated_tokens.cached_tokens += token_usage.cached_tokens
                aggregated_tokens.reasoning_tokens += token_usage.reasoning_tokens

        except (ContentFilterError, LenghtReasonError) as e:
            logging.error(
                "Error transcribing image: %s", str(e))
            raise e

        except Exception as e:
            logging.error("Error transcribing image: %s", e)
            raise e

        return aggregated_result, aggregated_tokens

    async def transcribe(self, image_url: str, specific_prompt: str = None) -> tuple[TranscribeAiResponse, TokensUsage]:
        """
        Transcribe the content of an image to text.
        Returns:
            tuple: (TranscribeAiResponse, token_usage_dict)
        """

        logging.info("Transcribing image..")

        try:
            instruction = specific_prompt or "transcribe the content of the image without making any corrections or assumptions."
            with get_openai_callback() as cb:
                translation = await self.chain.ainvoke(
                    {"encoded_image_url": image_url, "transcribe_instruction": instruction})
                token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

            return translation, token_usage

        except Exception as e:
            logging.error("Error transcribing image: %s", e)

            error_msg = str(e).lower()
            if "content filter" in error_msg or "blocked" in error_msg or "jailbreak" in error_msg:
                logging.error(
                    "Raising ContentFilterError")
                raise ContentFilterError() from e

            if " length limit was reached" in error_msg:
                logging.error(
                    "Raising LenghtReasonError")
                raise LenghtReasonError() from e

            return None, None
