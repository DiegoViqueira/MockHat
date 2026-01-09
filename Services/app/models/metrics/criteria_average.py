"""Model Criteria Distribution"""
from typing import Dict

from pydantic import BaseModel, Field


class CriteriaAverage(BaseModel):
    """Model Criteria Average"""
    # clave: criterio, valor: puntaje promedio
    criteria_scores: Dict[str, float] = Field(
        default_factory=dict, description="Puntajes promedio por criterio")
