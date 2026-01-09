"""Model Classroom"""
from datetime import datetime, UTC
from typing import List, Optional
from beanie import Document
from pymongo import IndexModel
from pydantic import Field
from pydantic import BaseModel
import ulid
from app.enums.institution import Institution
from app.enums.level import Level
from app.models.student import Student
from app.models.user import User


class Class(Document):
    """Modelo de documento para gestionar clases y sus estudiantes asociados."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    account_id: str = Field(default="")
    name: str = Field(default="")
    description: Optional[str] = Field(default=None)
    institution: Institution = Field(default=Institution.CAMBRIDGE)
    level: Level = Field(default=Level.B1)
    teachers: List[User] = Field(default_factory=list)
    students: List[Student] = Field(default_factory=list)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Configuración de la colección de clases."""
        name = "classes"
        indexes = [
            IndexModel(
                [("account_id", 1), ("name", 1)],
                unique=True
            ),
            [
                ("account_id", 1),
            ]
        ]


class ListClass(BaseModel):
    """List of classes with total count."""
    classes: List[Class]
    total: int
