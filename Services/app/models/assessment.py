"""Model Assessment"""
from datetime import datetime, UTC
from typing import List, Optional
from beanie import Document
from pydantic import Field
from pydantic import BaseModel
from pymongo import IndexModel
import pymongo
import ulid

from app.enums.exam_type import ExamType
from app.enums.institution import Institution
from app.enums.level import Level
from app.models.token_usage import TokensUsage
from app.enums.assessment_state import AssessmentState
from app.enums.writing_task import WritingTask


class Assessment(Document):
    """Modelo de documento para gestionar evaluaciones."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    account_id: str = Field(default="")
    class_id: str = Field(default="")
    user_id: str = Field(default="")
    level: Level = Field(default=Level.B1)
    institution: Institution = Field(default=Institution.CAMBRIDGE)
    exam_type: ExamType = Field(default=ExamType.CEQ)
    task: WritingTask = Field(default=WritingTask.EMAIL)
    title: str = Field(default="")
    description: Optional[str] = Field(default=None)
    image_url: str = Field(default="")
    image_text: str = Field(default="")
    image_transcription_tokens_usage: TokensUsage = Field(
        default=TokensUsage())
    state: AssessmentState = Field(default=AssessmentState.PENDING)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Configuración de la colección de evaluaciones."""
        name = "assessments"
        indexes = [
            IndexModel(
                [("account_id", 1), ("class_id", 1), ("title", 1)],
                unique=True
            ),
            [
                ("account_id", 1),
                ("class_id", 1),
            ],
        ]


class ListAssessment(BaseModel):
    """Lista de evaluaciones con total."""
    assessments: List[Assessment]
    total: int
