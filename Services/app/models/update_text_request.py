from pydantic import BaseModel


class UpdateAssessmentTextRequest(BaseModel):
    """Update assessment text request."""
    text: str
