from pydantic import BaseModel
from resources.WritingCriteriaScore import WritingCriteriaScore


class WritingResult(BaseModel):
    criteria: list[WritingCriteriaScore]
