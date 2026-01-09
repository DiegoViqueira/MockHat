"""Model Student Metrics"""

from typing import List
from pydantic import BaseModel, Field


class ScoreEntry(BaseModel):
    """Represents a single score entry for a specific date."""
    criteria: str = Field(
        default="", description="Criteria of the score")
    score: float = Field(
        default=0.0, description="Score obtained on the given date")


class AssessmentMetrics(BaseModel):
    """Metrics related to a specific evaluation criterion."""
    date: str = Field(
        default="", description="Date when the assessment was made")
    scores: List[ScoreEntry] = Field(
        default=[], description="List of score entries for this criterion")

    grammar_errors: int = Field(
        default=0, description="Number of grammar errors")


class AssessmentsMetrics(BaseModel):
    """Aggregated metrics for all evaluation criteria."""
    assessments: List[AssessmentMetrics] = Field(
        default=[], description="Metrics for each evaluation criterion")
    count: int = Field(
        default=0, description="Number of assessments")
    score_average: float = Field(
        default=0.0, description="Average score for all assessments")
    grammar_errors_average: float = Field(
        default=0.0, description="Average number of grammar errors for all assessments")
    pass_rate: int = Field(
        default=0, description="Pass rate for all assessments")


class StudentMetrics(BaseModel):
    """Metrics for a specific student, including all assessments."""
    name: str = Field(default="", description="Student's full name")
    assessments: AssessmentsMetrics = Field(
        default=AssessmentsMetrics(), description="Evaluation metrics by criteria")
