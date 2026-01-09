"""Exam Type"""
from enum import Enum


class ExamType(Enum):
    """Enum for the different types of exams."""
    CEQ = 'ceq'
    IELTS = 'ielts'
    LINGUA_SKILL = 'linguaSkill'
    ICAO = 'icao'
    EBAU = 'ebau'
