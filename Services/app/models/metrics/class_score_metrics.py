"""Model Class Score Metrics"""
from pydantic import BaseModel, Field


class ClassScoreMetrics(BaseModel):
    average_score: float = Field(
        default=0.0, description="average of scores")
    pass_rate: float = Field(
        default=0.0, description="percentage of passed students")
    avg_grammar_errors: float = Field(
        default=0.0, description="average of grammar errors")
