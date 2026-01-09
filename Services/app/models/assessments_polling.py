from typing import List
from pydantic import BaseModel


class AssessmentsPolling(BaseModel):
    """Assessments polling model."""
    count: int
    assessments: List[str]
