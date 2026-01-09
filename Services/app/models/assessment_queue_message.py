"""Assessment queue message"""
from pydantic import BaseModel, Field


class AssessmentQueueMessage(BaseModel):
    """Assessment queue message"""
    assessment_id: str = Field(...)
    language: str = Field(default="en")
