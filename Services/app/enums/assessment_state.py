"""Assessment State"""
from enum import Enum


class AssessmentState(Enum):
    """Estado de la evaluación."""
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"
    ERROR = "error"
