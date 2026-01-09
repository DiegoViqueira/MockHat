"""Model Transcribe AI Response"""
from pydantic import BaseModel, Field


class TranscribeAiResponse(BaseModel):
    """
    Transcribe AI response model.
    """

    text: str = Field(..., description="Text extracted from the image")
