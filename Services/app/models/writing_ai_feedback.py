"""Model Writing AI Feedback"""
from typing import List
from pydantic import BaseModel, Field

from app.models.writing_criteria_score import WritingCriteriaScore
from app.models.token_usage import TokensUsage


class WritingAIFeedback(BaseModel):
    """Model representing the AI feedback for a writing task."""
    criterias: List[WritingCriteriaScore] = Field([])
    spent_tokens: TokensUsage = Field(default=TokensUsage())
