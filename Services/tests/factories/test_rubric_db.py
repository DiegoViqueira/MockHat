import pytest
from app.databases.rubric_db import RubricDB
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask


class TestRubricDB:
    """Integration tests for RubricDB class with actual files."""

    @pytest.fixture
    def rubric_db(self):
        """Create a RubricDB instance for testing."""
        return RubricDB()

    def test_load_database_loads_all_files(self, rubric_db):
        """Test that the database loads all available files."""
        assert len(rubric_db.db) == 19, "No rubric files were loaded"

    def test_all_combinations_exist(self, rubric_db):
        """Test that all combinations that should exist do exist."""
        combinations = [
            (Institution.CAMBRIDGE, Level.B1, WritingTask.EMAIL),
            (Institution.CAMBRIDGE, Level.B1, WritingTask.ARTICLE),
            (Institution.CAMBRIDGE, Level.B1, WritingTask.STORY),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.ARTICLE),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.EMAIL),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.ESSAY),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.REPORT),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.REVIEW),
            (Institution.CAMBRIDGE, Level.B2, WritingTask.STORY),
            (Institution.CAMBRIDGE, Level.C1, WritingTask.EMAIL),
            (Institution.CAMBRIDGE, Level.C1, WritingTask.ESSAY),
            (Institution.CAMBRIDGE, Level.C1, WritingTask.PROPOSAL),
            (Institution.CAMBRIDGE, Level.C1, WritingTask.REPORT),
            (Institution.CAMBRIDGE, Level.C1, WritingTask.REVIEW),
            (Institution.BACHILLERATO, Level.EBAU,
             WritingTask.FORMAL_APPLICATION_EMAIL),
            (Institution.BACHILLERATO, Level.EBAU,
             WritingTask.FORMAL_COMPLAINT_EMAIL),
            (Institution.BACHILLERATO, Level.EBAU, WritingTask.INFORMAL_EMAIL),
            (Institution.BACHILLERATO, Level.EBAU, WritingTask.OPINION_ESSAY),
            (Institution.BACHILLERATO, Level.EBAU,
             WritingTask.FOR_AND_AGAINST_ESSAY),
        ]

        for institution, level, task in combinations:
            example = rubric_db.get_rubric(
                institution, level, task)
            assert example is not None, f"{institution.value} {level.value} {task.value} example not found"
            assert isinstance(
                example, str), f"{institution.value} {level.value} {task.value} example is not a string"
