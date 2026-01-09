from pydantic import BaseModel


class WritingCriteriaScore(BaseModel):
    criteria: str
    score: int
    feedback: str
