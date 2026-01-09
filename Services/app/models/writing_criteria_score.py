"""Model Writing Criteria Score"""
from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional


class WritingCriteriaScore(BaseModel):
    """Model representing a score for a writing criteria."""
    criteria: str = Field(
        description="The criteria of the score.")
    score: float = Field(
        description="The score of the criteria.")
    max_score: Optional[float] = Field(default=None,
                                       description="The maximum score of the criteria.")
    feedback: str = Field(
        description="The feedback of the criteria.")
