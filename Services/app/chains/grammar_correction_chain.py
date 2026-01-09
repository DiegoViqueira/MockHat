"""Grammar Correction Chain"""
import logging

from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.output_parsers import PydanticOutputParser
from langchain_community.callbacks.manager import get_openai_callback

from app.chains import GRAMMAR_CORRECTION_PROMPT
from app.enums.deployment import Deployment
from app.factories.language_model_factory import ModelEngine
from app.models.token_usage import TokensUsage
from app.models.gramar import GammarAi
from app.handlers.debug_messages_handler import DebugMessagesHandler
from app.errors.content_filter_error import ContentFilterError
from app.errors.lenght_reason_error import LenghtReasonError


class GrammarCorrectionChain:
    """
    A chain that corrects writing errors in a text.
    """

    def __init__(self, model: ModelEngine):
        self.model = model
        self.llm = model.model
        self.structured_llm = self.llm.with_structured_output(GammarAi)
        self.parser = PydanticOutputParser(pydantic_object=GammarAi)
        self.using_parser = model.deployment != Deployment.GPT_4O and model.deployment != Deployment.GPT_41
        self._build_prompt_templates()
        self.chain = self._build_chain()
        self.chain = self.chain.with_config(callbacks=[DebugMessagesHandler()])

    def _build_prompt_templates(self):

        self.format_prompt = HumanMessage(
            content=f"Parse as follows: {self.parser.get_format_instructions()}")

    def _build_chain(self):
        logging.info("Using model %s %s", self.model.provider,
                     self.model.deployment)
        prompts = [GRAMMAR_CORRECTION_PROMPT]

        if self.using_parser:
            logging.info("Using Parser")
            prompts.append(self.format_prompt)
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.llm | self.parser
        else:
            logging.info("Using Structured Output")
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.structured_llm

    async def run(self, text_to_evaluate: str, extra_prompt: str | None = None, grammar_reference: str | None = None) -> tuple[GammarAi, TokensUsage]:
        """
        Run the chain.
        """

        # self.final_grammar_correction_prompt.pretty_print()

        extra_prompt = extra_prompt or ""
        grammar_reference = grammar_reference or ""
        try:
            with get_openai_callback() as cb:

                grammar = await self.chain.ainvoke(
                    {"text_to_evaluate": text_to_evaluate, "extra_prompt": extra_prompt, "grammar_reference": grammar_reference})
                grammar_token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

            return grammar, grammar_token_usage

        except Exception as e:

            error_msg = str(e).lower()
            if "content filter" in error_msg or "blocked" in error_msg:
                raise ContentFilterError() from e

            if "length limit was reached" in error_msg:
                raise LenghtReasonError() from e

            logging.error("Error running grammar correction chain: %s", e)
            return None, None
