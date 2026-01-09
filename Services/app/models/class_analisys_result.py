
from pydantic import BaseModel, Field


class ClassAnalysisResult(BaseModel):
    """
    The result of the class analysis
    """
    summary: str = Field(description="The summary of the class analysis")
