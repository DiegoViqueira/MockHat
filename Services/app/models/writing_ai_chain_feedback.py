"""Model Writing AI Chain Feedback"""
from typing import List
from pydantic import BaseModel, Field

from app.models.writing_criteria_score import WritingCriteriaScore


class WritingAIChainFeedback(BaseModel):
    """Model representing the AI feedback for a writing task."""
    criterias: List[WritingCriteriaScore] = Field(
        description="The list of criteria scores.")
