"""EvaluationState"""
import operator

from typing import Annotated
from pydantic import BaseModel, Field
from app.models.token_usage import TokensUsage
from pocs.agents.models.consolidated_report import ConsolidatedReport
from pocs.agents.models.evaluation_criteria import EvaluationCriteria
from pocs.agents.models.evaluator_report import EvaluatorReport
from pocs.agents.models.research import Research
from pocs.agents.models.student_response import StudentResponse


def combine_criteria(a: list[EvaluationCriteria], b: list[EvaluationCriteria]) -> list[EvaluationCriteria]:
    """Combina las listas evitando duplicados"""
    combined = a + [section for section in b if section not in a]
    return combined


def combine_reports(a: list[EvaluatorReport], b: list[EvaluatorReport]) -> list[EvaluatorReport]:
    """Combina las listas evitando duplicados"""
    combined = a + [report for report in b if report not in a]
    return combined


def combine_consolidated_reports(a: list[ConsolidatedReport], b: list[ConsolidatedReport]) -> list[ConsolidatedReport]:
    """Combina las listas evitando duplicados"""
    combined = a + [report for report in b if report not in a]
    return combined


def combine_student_responses(a: list[StudentResponse], b: list[StudentResponse]) -> list[StudentResponse]:
    """Combina las listas evitando duplicados"""
    combined = a + [response for response in b if response not in a]
    return combined


def combine_research(a: list[Research], b: list[Research]) -> list[Research]:
    """Combina las listas evitando duplicados"""
    combined = a + [research for research in b if research not in a]
    return combined


class EvaluationState(BaseModel):
    """Evaluation state."""
    evaluation_criteria: Annotated[list[EvaluationCriteria], combine_criteria] = Field(
        default_factory=list)
    evaluator_reports: Annotated[list[EvaluatorReport],
                                 combine_reports] = Field(default_factory=list)
    student_responses: Annotated[list[StudentResponse],
                                 combine_student_responses] = Field(
        default_factory=list)
    consolidated_reports: Annotated[list[ConsolidatedReport],
                                    combine_consolidated_reports] = Field(
        default_factory=list)
    research: Annotated[list[Research],
                        combine_research] = Field(default_factory=list)
    final_consolidated_report: Annotated[str,
                                         operator.add] = Field(default="")
    tokens_usage: Annotated[TokensUsage,
                            operator.add] = Field(default=TokensUsage())
