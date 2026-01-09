import pytest
from app.databases.few_shot_writing_db import FewShotWritingDB
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask


class TestFewShotWritingDB:
    """Integration tests for FewShotWritingDB class with actual files."""

    @pytest.fixture
    def few_shot_db(self):
        """Create a FewShotWritingDB instance for testing."""
        return FewShotWritingDB()

    def test_load_database_loads_all_files(self, few_shot_db):
        """Test that the database loads all available files."""
        # Verificamos que se carguen al menos algunos ejemplos
        assert len(few_shot_db.db) > 0, "No few-shot examples were loaded"

    def test_all_combinations_exist(self, few_shot_db):
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
            example = few_shot_db.get_few_shot_writing(
                institution, level, task)
            assert example is not None, f"{institution.value} {level.value} {task.value} example not found"

            # assert "assigned_task" in example, "Missing assigned_task field"
            # assert "task_answer" in example, "Missing task_answer field"
            # assert "ai_answer" in example, "Missing ai_answer field"
