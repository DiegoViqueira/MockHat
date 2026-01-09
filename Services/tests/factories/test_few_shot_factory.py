"""Test FewShotWritingFactory"""
from unittest.mock import patch
import pytest

from langchain.prompts import ChatPromptTemplate
from app.factories.few_shot_factory import FewShotWritingFactory
from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask


class TestFewShotWritingFactory:
    """Tests for the FewShotWritingFactory class."""

    @pytest.fixture
    def few_shot_factory(self):
        """Create a FewShotWritingFactory instance for testing."""
        return FewShotWritingFactory()

    def test_init(self, few_shot_factory):
        """Test that the factory initializes correctly."""
        assert isinstance(few_shot_factory.few_shot_prompt, ChatPromptTemplate)
        assert hasattr(few_shot_factory, 'few_shot_db')

    def test_get_few_shot_prompt_invalid_combination(self, few_shot_factory):
        """Test that an error is raised for an invalid combination."""
        # Create a mock for few_shot_db.get_few_shot_writing that returns None
        with patch.object(few_shot_factory.few_shot_db, 'get_few_shot_writing', return_value=None):
            with pytest.raises(ValueError) as excinfo:
                few_shot_factory.get_few_shot_prompt(
                    Level.C2, Institution.CAMBRIDGE, WritingTask.EMAIL)

            # Check the error message
            assert "No few shot sample found" in str(excinfo.value)

    def test_get_few_shot_prompt_formats_correctly(self, few_shot_factory):
        """Test that the prompt is formatted correctly with the sample data."""
        # Create a mock sample
        mock_sample = {
            "assigned_task": "Write an email to a friend",
            "task_answer": "Dear friend, I am writing to tell you...",
            "ai_answer": [
                {"criteria": "Content", "score": 4.0, "feedback": "Good content"},
                {"criteria": "Language", "score": 3.0, "feedback": "Some errors"}
            ]
        }

        # Mock the database call
        with patch.object(few_shot_factory.few_shot_db, 'get_few_shot_writing', return_value=mock_sample):
            messages = few_shot_factory.get_few_shot_prompt(
                Level.B2, Institution.CAMBRIDGE, WritingTask.EMAIL)

            # Check that the content is correctly formatted
            assert "Write an email to a friend" in messages[0].content
            assert "Dear friend, I am writing to tell you..." in messages[1].content
            assert "Content" in messages[2].content
            assert "Good content" in messages[2].content
            assert "Language" in messages[2].content
            assert "Some errors" in messages[2].content

    def test_integration_with_few_shot_db(self, few_shot_factory):
        """Test the integration with FewShotWritingDB."""
        # Test with all combinations from our test_few_shot_writing_db
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
            # (Institution.EBAU, Level.EBAU, WritingTask.FORMAL_APPLICATION_EMAIL),
            # (Institution.EBAU, Level.EBAU, WritingTask.FORMAL_COMPLAINT_EMAIL),
            # (Institution.EBAU, Level.EBAU, WritingTask.INFORMAL_EMAIL),
            # (Institution.EBAU, Level.EBAU, WritingTask.OPINION_ESSAY),
            # (Institution.EBAU, Level.EBAU, WritingTask.FOR_AND_AGAINST_ESSAY),
        ]

        for institution, level, task in combinations:
            try:
                messages = few_shot_factory.get_few_shot_prompt(
                    institution, level, task)

                assert isinstance(messages, list)
                assert len(messages) == 3
            except ValueError as e:
                pytest.fail(
                    f"Failed to get prompt for {institution.value} {level.value} {task.value}: {e}")
