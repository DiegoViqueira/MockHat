"""Model Student"""
from datetime import datetime, UTC
from typing import Optional
from beanie import Document
from pydantic import Field
import ulid
from pymongo import IndexModel


class Student(Document):
    """Model for storing student information."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()),
                    description="The ID of the student")
    name: str = Field(default="", description="The name of the student")
    last_name: str = Field(
        default="", description="The last name of the student")
    account_id: str = Field(..., description="The account ID of the student")
    email: Optional[str] = Field(
        default=None, description="The email of the student")
    active: bool = Field(
        default=True, description="Whether the student is active")
    created_at: datetime = Field(default_factory=lambda: datetime.now(
        UTC), description="The date and time the student was created")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(
        UTC), description="The date and time the student was last updated")

    class Settings:
        """Settings for the students collection."""
        name = "students"
        indexes = [
            IndexModel(
                [("account_id", 1), ("name", 1), ("last_name", 1)],
                unique=True
            ),
            [
                ("account_id", 1),
            ]
        ]

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.id == other.id
        return False
