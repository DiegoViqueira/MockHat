"""Writing State"""
from enum import Enum


class WritingState(Enum):
    """Enum para los estados de escritura."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    ERROR = "Error"
