"""ConsolidatedReport"""
from pydantic import BaseModel, Field

from app.models.token_usage import TokensUsage


class ConsolidatedReport(BaseModel):
    """Consolidated report."""
    section_name: str = Field(default="")
    report: str = Field(default="")
    tokens_usage: TokensUsage = Field(default=TokensUsage())
