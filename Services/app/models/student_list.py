"""Model Student List"""
from app.models.student import Student


from pydantic import BaseModel


from typing import List


class StudentList(BaseModel):
    """List of students."""
    students: List[Student]
    total: int
