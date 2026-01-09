"""Writing Correction Chain"""
import logging
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import HumanMessage
from langchain_community.callbacks.manager import get_openai_callback


from app.chains import WRITING_CORRECTION_PROMPT
from app.enums.deployment import Deployment
from app.factories.language_model_factory import ModelEngine
from app.models.token_usage import TokensUsage
from app.enums.level import Level
from app.enums.institution import Institution
from app.enums.writing_task import WritingTask
from app.handlers.debug_messages_handler import DebugMessagesHandler
from app.models.writing_ai_chain_feedback import WritingAIChainFeedback
from app.errors.content_filter_error import ContentFilterError
from app.errors.lenght_reason_error import LenghtReasonError


class WritingCorrectionChain:
    """
    A chain that corrects writing errors in a text.
    """

    def __init__(self, model: ModelEngine):
        self.model = model
        self.llm = model.model
        self.parser = PydanticOutputParser(
            pydantic_object=WritingAIChainFeedback)
        self.structured_llm = self.llm.with_structured_output(
            WritingAIChainFeedback)
        self._build_prompt_templates()
        self.using_parser = model.deployment != Deployment.GPT_4O and model.deployment != Deployment.GPT_41
        self.chain = self._build_chain()
        self.chain = self.chain.with_config(callbacks=[DebugMessagesHandler()])

    def _build_prompt_templates(self):
        self.format_prompt = HumanMessage(
            content=f"Parse as follows: {self.parser.get_format_instructions()}")

    def _build_chain(self):
        logging.info("Using model %s %s", self.model.provider,
                     self.model.deployment)
        prompts = [
            WRITING_CORRECTION_PROMPT,
        ]

        if self.using_parser:
            logging.info("Using Parser")
            prompts.append(self.format_prompt)
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.llm | self.parser
        else:
            logging.info("Using Structured Output")
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.structured_llm

    async def run(self, level: Level, institution: Institution, task: WritingTask, rubric: str, grammar_correction: str, task_value: str, task_answer: str, task_answer_word_count: int, examples: ChatPromptTemplate) -> tuple[WritingAIChainFeedback, TokensUsage]:
        """
        Run the chain.
        """
        try:
            with get_openai_callback() as cb:
                invoke_params = {
                    "level": level.value,
                    "institution": institution.value,
                    "task": task.value,
                    "rubric": rubric,
                    "grammar_correction": grammar_correction,
                    "task_value": task_value,
                    "answer_words_count": task_answer_word_count,
                    "task_answer": task_answer,
                }

                # Only add examples if they are not None
                if examples is not None:
                    logging.info("Adding examples to invoke params")
                    invoke_params["examples"] = examples

                writing_feedback = await self.chain.ainvoke(invoke_params)

                writing_feedback_token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

            return writing_feedback, writing_feedback_token_usage
        except Exception as e:
            error_msg = str(e).lower()
            if "content filter" in error_msg or "blocked" in error_msg:
                raise ContentFilterError() from e

            if "length limit was reached" in error_msg:
                raise LenghtReasonError() from e

            logging.error("Error running writing correction chain: %s", e)
            return None, None
