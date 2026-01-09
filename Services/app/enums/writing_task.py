"""Writing Task"""
from enum import Enum


class WritingTask(Enum):
    """Enum para las tareas de escritura disponibles."""
    EMAIL = 'Email'
    ARTICLE = 'Article'
    STORY = 'Story'
    ESSAY = 'Essay'
    PROPOSAL = 'Proposal'
    REPORT = 'Report'
    REVIEW = 'Review'
    FOR_AND_AGAINST_ESSAY = 'ForAndAgainstEssay'
    FORMAL_APPLICATION_EMAIL = 'FormalApplicationEmail'
    FORMAL_COMPLAINT_EMAIL = 'FormalComplaintEmail'
    INFORMAL_EMAIL = 'InformalEmail'
    OPINION_ESSAY = 'OpinionEssay'
    LETTER = 'Letter'
