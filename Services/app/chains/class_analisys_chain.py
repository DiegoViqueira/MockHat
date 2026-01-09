"""
This module contains the chain that analyzes a class and returns a result
"""
import logging

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain_community.callbacks.manager import get_openai_callback

from app.enums.deployment import Deployment
from app.errors.content_filter_error import ContentFilterError
from app.factories.language_model_factory import ModelEngine
from app.models.class_analisys_result import ClassAnalysisResult
from app.chains import CLASS_ANALYSIS_PROMPT
from app.models.token_usage import TokensUsage


class ClassAnalisysChain:
    """
    A chain that analyzes a class and returns a result
    """

    def __init__(self, model: ModelEngine):
        self.model = model
        self.llm = model.model
        self.structured_llm = self.llm.with_structured_output(
            ClassAnalysisResult)
        self.parser = PydanticOutputParser(pydantic_object=ClassAnalysisResult)
        self.using_parser = model.deployment != Deployment.GPT_4O and model.deployment != Deployment.GPT_41
        self.chain = self._build_chain()

    def _build_chain(self):
        """
        Build the class analysis chain
        """
        prompts = [CLASS_ANALYSIS_PROMPT]

        self.format_prompt = HumanMessage(
            content=f"Parse as follows: {self.parser.get_format_instructions()}")

        if self.using_parser:
            logging.info("Using Parser")
            prompts.append(self.format_prompt)
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.llm | self.parser
        else:
            logging.info("Using Structured Output")
            prompt_template = ChatPromptTemplate.from_messages(prompts)
            return prompt_template | self.structured_llm

    def _build_messages(self, messages: list[str]) -> list[AIMessage]:
        """
        Build the messages for the class analysis chain
        """
        return [AIMessage(content=message) for message in messages]

    async def run(self, messages: list[str]) -> tuple[ClassAnalysisResult, TokensUsage]:
        """
        Run the class analysis chain
        """
        logging.info("Running class analysis chain")
        try:
            with get_openai_callback() as cb:
                invoke_params = {
                    "messages": self._build_messages(messages),
                }

                class_analysis = await self.chain.ainvoke(invoke_params)

                class_analysis_token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

                return class_analysis, class_analysis_token_usage

        except Exception as e:
            error_msg = str(e).lower()
            if "content filter" in error_msg or "blocked" in error_msg:
                raise ContentFilterError() from e
            logging.error("Error running class analysis chain: %s", e)
            return None, None
