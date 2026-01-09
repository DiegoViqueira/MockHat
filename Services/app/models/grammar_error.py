"""Model Grammar Error"""
from pydantic import BaseModel, Field


class GrammarError(BaseModel):
    """Grammar error model."""
    error_text: str = Field(description="The text with the grammar error.")
    corrected_text: str = Field(description="The corrected text.")
    correction_explanation: str = Field(
        description="The explanation of the correction.")
