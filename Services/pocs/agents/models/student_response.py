from pydantic import BaseModel, Field


class StudentResponse(BaseModel):
    """Evaluation student response."""
    section_name: str = Field(default="")
    response: str = Field(default="")
