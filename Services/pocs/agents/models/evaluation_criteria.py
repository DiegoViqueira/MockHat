"""EvaluationCriteria"""
from pydantic import BaseModel, Field


class EvaluationCriteria(BaseModel):
    """Evaluation criteria."""
    section_name: str = Field(default="")
    criteria: str = Field(default="")
    enunciation: str = Field(default="")
