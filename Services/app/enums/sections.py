"""Sections"""
from enum import Enum


class Section(Enum):
    """Enum for the different sections of the exam."""
    READING = "Reading"
    WRITING = "Writing"
    LISTENING = "Listening"
    SPEAKING = "Speaking"
    USE_OF_ENGLISH = "UseOfEnglish"
