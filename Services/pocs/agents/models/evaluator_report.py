"""EvaluatorReport"""

from pydantic import BaseModel, Field

from app.models.token_usage import TokensUsage


class EvaluatorReport(BaseModel):
    """Evaluation evaluator report."""
    section_name: str = Field(default="")
    evaluator_name: str = Field(default="")
    report: str = Field(default="")
    tokens_usage: TokensUsage = Field(default=TokensUsage())
