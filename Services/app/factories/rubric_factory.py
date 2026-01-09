"""Rubric Factory"""
from app.databases.rubric_db import RubricDB
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask


class RubricFactory:
    """Factory class for creating rubrics."""

    def __init__(self):
        self.rubric_db = RubricDB()

    def get_rubric(self, institution: Institution, level: Level, task: WritingTask) -> str:
        """Get the rubric for the given institution, level and task.

        Args:
            institution: The institution (e.g., CAMBRIDGE)
            level: The proficiency level (e.g., B1)
            task: The writing task type (e.g., Email)

        Returns:
            String containing the rubric for the given institution, level and task
        """
        return self.rubric_db.get_rubric(institution, level, task)
