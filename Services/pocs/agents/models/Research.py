"""Research"""
from pydantic import BaseModel, Field


class Research(BaseModel):
    """Research."""
    section_name: str = Field(description="Nombre de la sección.")
    research: str = Field(description="Research del contenido.")
