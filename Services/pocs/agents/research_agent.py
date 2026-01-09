"""ResearchAgent"""
import logging

from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

from pocs.agents.models.evaluation_state import EvaluationState
from pocs.agents.models.research import Research
from pocs.agents.models.student_response import StudentResponse
from pocs.core.prompts import RESEARCH_PROMPT
from pocs.core.tools.tools import duckduckgo_search_tool, wikipedia_search_tool


class ResearchAgent:
    """Research agent."""

    def __init__(self, model, name: str):
        self.model = model
        self.name = name
        self.tools = [
            duckduckgo_search_tool,
            wikipedia_search_tool
        ]
        self.agent = create_react_agent(model, tools=self.tools)

    def _create_prompt(self, student_response: StudentResponse):

        return [
            SystemMessage(content=RESEARCH_PROMPT),
            HumanMessage(
                content=f"Realiza una investigacion sobre el siguiente contenido: {student_response.response}"),
        ]

    def run(self, state: EvaluationState, part_name: str = None) -> EvaluationState:
        """Run the research agent."""

        logging.info("Ejecutando Research para AGENTE[%s] - PARTE[%s] ",
                     self.name, part_name)

        student_response = next(
            (response for response in state.student_responses if response.section_name == part_name), None)

        initial_state = {
            "messages": self._create_prompt(student_response),
        }

        response = self.agent.invoke(initial_state)

        research = Research(
            section_name=part_name,
            research=response["messages"][-1].content
        )

        state.research.append(research)

        return state
