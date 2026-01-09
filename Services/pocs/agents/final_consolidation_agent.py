"""Final consolidation agent"""
import logging
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate
from app.models.token_usage import TokensUsage
from pocs.agents.models.evaluation_state import EvaluationState
from pocs.core.prompts import FINAL_CONSOLIDATOR_PROMPT


class FinalConsolidationAgent:
    """Agente encargado de consolidar las evaluaciones de ambas partes."""

    def __init__(self, model):
        self.model = model
        self.prompt_template = self._create_prompt_template()

    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Crea el template del prompt para la consolidación final."""
        system_prompt = SystemMessagePromptTemplate.from_template(
            FINAL_CONSOLIDATOR_PROMPT)
        return ChatPromptTemplate.from_messages([system_prompt])

    def run(self, state: EvaluationState, part_name: str = None) -> EvaluationState:
        """
        Ejecuta el agente de consolidación final.
        """
        try:
            logging.info("Consolidación final para PARTE[%s] ", part_name)
            # Obtener los reportes consolidados de ambas partes

            parta_report = next(
                (report for report in state.consolidated_reports if report.section_name == "PARTA"), None)
            partb_report = next(
                (report for report in state.consolidated_reports if report.section_name == "PARTB"), None)

            chain = self.prompt_template | self.model

            response = chain.invoke({
                "parta_report": parta_report,
                "partb_report": partb_report
            })

            state.final_consolidated_report = response.content
            state.tokens_usage = TokensUsage(
                prompt_tokens=response.usage_metadata.get("input_tokens", 0),
                completion_tokens=response.usage_metadata.get(
                    "output_tokens", 0),
                total_tokens=response.usage_metadata.get("total_tokens", 0),
                total_cost=0,
                cached_tokens=0,
            )

            return state

        except Exception as e:
            logging.error(
                "Error en agente de consolidación final: %s", str(e)[:100])
            return state
