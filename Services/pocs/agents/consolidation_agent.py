"""Consolidation Agent"""
import logging
from typing import List
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage
from langchain_community.callbacks.manager import get_openai_callback
from pydantic import BaseModel, Field

from app.models.token_usage import TokensUsage
from pocs.agents.models.consolidated_report import ConsolidatedReport
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.core.prompts import CONSOLIDATOR_PROMPT


class Score(BaseModel):
    """Score for evaluation."""
    criterio: str = Field(description="Criterio Evaluado.")
    score: float = Field(description="Puntuación asignada.")
    razon: str = Field(description="Justificación de la puntuación.")


class ConsolidationAgentReport(BaseModel):
    """Consolidation report."""
    informe: str = Field(
        description="Informe de la consolidación EN MARKDOWN.")
    puntuaciones: List[Score] = Field(
        description="Puntuaciones asignadas a cada criterio.")
    fuentes: List[str] = Field(description="Fuentes externas utilizadas URLs.")


class ConsolidationAgent:
    """Consolidation agent responsible for consolidating evaluations."""

    def __init__(self, model):
        self.model = model
        self.parser = PydanticOutputParser(
            pydantic_object=ConsolidationAgentReport)
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Creates the prompt template for consolidation."""
        system_prompt = SystemMessagePromptTemplate.from_template(
            CONSOLIDATOR_PROMPT)
        parser_instructions = HumanMessage(
            content=f"Parse as follows: {self.parser.get_format_instructions()}")
        return ChatPromptTemplate.from_messages([system_prompt, parser_instructions])

    def run(self, state: EvaluationState, part_name: str = None) -> EvaluationState:
        """Executes the consolidation agent."""
        try:
            logging.info("Consolidación para PARTE[%s] ", part_name)
            chain = self.prompt_template | self.model | self.parser

            evaluator_1_response = None
            evaluator_2_response = None

            for report in state.evaluator_reports:
                if report.section_name == part_name:
                    if report.evaluator_name == "A":
                        evaluator_1_response = report.report
                    elif report.evaluator_name == "B":
                        evaluator_2_response = report.report
                    break

            with get_openai_callback() as cb:
                response = chain.invoke({
                    "evaluator_1_response": evaluator_1_response,
                    "evaluator_2_response": evaluator_2_response
                })

                consolidated_report_token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

            consolidated_report = ConsolidatedReport(
                section_name=part_name,
                report=response.model_dump_json(),
                tokens_usage=consolidated_report_token_usage
            )

            state.consolidated_reports.append(consolidated_report)

        except Exception as e:
            logging.error("Error in consolidation agent: %s", str(e)[:100])
        return state
