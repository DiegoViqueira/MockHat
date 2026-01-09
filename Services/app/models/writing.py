"""Model Writing"""
from datetime import datetime, UTC
from typing import List, Optional

from beanie import Document
from pydantic import Field, BaseModel
import ulid
from app.models.user import User
from app.models.writing_ai_feedback import WritingAIFeedback
from app.enums.writing_state import WritingState
from app.enums.writing_task import WritingTask
from app.enums.exam_type import ExamType
from app.enums.institution import Institution
from app.enums.level import Level
from app.models.token_usage import TokensUsage
from app.models.gramar import Grammar
from app.models.student import Student


class Writing(Document):
    """Model representing a writing task."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    assessment_id: str = Field(...)
    class_id: str = Field(...)
    student_id: str = Field(...)
    account_id: str = Field(...)
    user_id: str = Field(...)
    level: Level = Field(default=Level.B1)
    institution: Institution = Field(default=Institution.CAMBRIDGE)
    exam_type: ExamType = Field(default=ExamType.CEQ)
    task: WritingTask = Field(default=WritingTask.EMAIL)
    student_response_image_urls: List[str] = Field(default=[])
    student_response_text: str = Field(default="")
    student_response_word_count: Optional[int] = Field(default=None)
    student_response_tokens_usage: TokensUsage = Field(default=TokensUsage())
    grammar_feedback: Grammar = Field(default=Grammar())
    grammar_feedback_tokens_usage: TokensUsage = Field(default=TokensUsage())
    ai_feedback: WritingAIFeedback = Field(default=WritingAIFeedback())
    writing_state: WritingState = Field(default=WritingState.PENDING)
    error_message: str = Field(default="")
    writing_score: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Configuration of the writing collection."""
        name = "writings"
        indexes = [
            [
                ("user_id", 1),
            ],
            [
                ("assessment_id", 1),
                ("account_id", 1),
            ],
        ]


class WritingDto(BaseModel):
    """Model representing a writing task."""
    id: str = Field(default="")
    assessment_id: str = Field(default="")
    class_id: str = Field(default="")
    student: Student | None = Field(default=None)
    account_id: str = Field(default="")
    user: User | None = Field(default=None)
    level: Level = Field(default=Level.B1)
    institution: Institution = Field(default=Institution.CAMBRIDGE)
    exam_type: ExamType = Field(default=ExamType.CEQ)
    task: WritingTask = Field(default=WritingTask.EMAIL)
    student_response_image_urls: List[str] = Field(default=[])
    student_response_text: str = Field(default="")
    student_response_word_count: Optional[int] = Field(default=None)
    student_response_tokens_usage: TokensUsage = Field(default=TokensUsage())
    grammar_feedback: Grammar = Field(default=Grammar())
    grammar_feedback_tokens_usage: TokensUsage = Field(default=TokensUsage())
    ai_feedback: WritingAIFeedback = Field(default=WritingAIFeedback())
    writing_state: WritingState = Field(default=WritingState.PENDING)
    error_message: str = Field(default="")
    writing_score: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
