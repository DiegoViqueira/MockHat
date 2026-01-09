"""Evaluation agent"""
import logging
from typing import List
from pydantic import BaseModel, Field

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from langchain_community.callbacks.manager import get_openai_callback

from app.models.token_usage import TokensUsage
from pocs.agents.models.evaluation_criteria import EvaluationCriteria
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.agents.models.evaluator_report import EvaluatorReport
from pocs.agents.models.research import Research
from pocs.agents.models.student_response import StudentResponse
from pocs.core.prompts import EVALUATOR_PROMPT


class Score(BaseModel):
    """Score for evaluation."""
    criterio: str = Field(description="Criterio Evaluado.")
    score: float = Field(description="Puntuación asignada.")
    razon: str = Field(description="Justificación de la puntuación.")


class EvaluationAgentReport(BaseModel):
    """Consolidation report."""
    informe: str = Field(
        description="Informe de la evaluación EN MARKDOWN **SOLO PARA ESTE CAMPO**.")
    puntuaciones: List[Score] = Field(
        description="Puntuaciones asignadas a cada criterio.")
    fuentes: List[str] = Field(description="Fuentes externas utilizadas.")


class EvaluationAgent:
    """Base class for evaluation agents."""

    def __init__(self, model, name: str):
        self.model = model
        self.name = name
        self.parser = PydanticOutputParser(
            pydantic_object=EvaluationAgentReport)

    def _create_prompt(self, criteria: EvaluationCriteria, student_response: StudentResponse, research: Research):

        messages = [
            SystemMessage(content=EVALUATOR_PROMPT),
            HumanMessage(
                content=f"Criterios de valoración: {criteria.criteria}"),
            HumanMessage(
                content=f"Sección: {criteria.section_name}"),
            HumanMessage(
                content=f"Enunciado: {criteria.enunciation}"),
            HumanMessage(
                content=f"Respuesta del alumno: {student_response.response}"),
            HumanMessage(
                content=f"Research del contenido: {research.research}"),
            HumanMessage(
                content=f"Parse ouput as follow: {self.parser.get_format_instructions()}")
        ]

        return ChatPromptTemplate.from_messages(messages)

    def run(self, state: EvaluationState, part_name: str = None) -> EvaluationState:
        """
        Ejecuta el agente de evaluación.
        """
        try:

            logging.info("Ejecutando Evaluación para AGENTE[%s] - PARTE[%s] ",
                         self.name, part_name)

            evaluation_criteria = next(
                (criteria for criteria in state.evaluation_criteria if criteria.section_name == part_name), None)

            research = next(
                (research for research in state.research if research.section_name == part_name), None)

            student_response = next(
                (response for response in state.student_responses if response.section_name == part_name), None)

            with get_openai_callback() as cb:
                chain = self._create_prompt(
                    evaluation_criteria, student_response, research) | self.model | self.parser

                evaluation_report = chain.invoke({"input": ""})

                evaluation_report_token_usage = TokensUsage(
                    prompt_tokens=cb.prompt_tokens,
                    completion_tokens=cb.completion_tokens,
                    total_tokens=cb.total_tokens,
                    total_cost=cb.total_cost,
                    cached_tokens=cb.prompt_tokens_cached,
                    reasoning_tokens=cb.reasoning_tokens
                )

            evaluator_report = EvaluatorReport(
                section_name=part_name,
                evaluator_name=self.name,
                report=evaluation_report.model_dump_json(),
                tokens_usage=evaluation_report_token_usage
            )

            state.evaluator_reports.append(evaluator_report)
            return state

        except Exception as e:
            logging.error("Error en agente evaluador %s: %s",
                          self.name, str(e))
            return state

    def _log_tool_usage(self, response: any) -> None:
        """Logs the tool usage."""

        tool_calls = 0
        for message in response:
            if isinstance(message, ToolMessage):
                tool_calls += 1

        if tool_calls == 0:
            logging.warning("%s did not use any tool", self.name)
        else:
            logging.info("%s used %s tools", self.name, tool_calls)
