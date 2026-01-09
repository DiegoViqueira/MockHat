"""Model Score Trends"""
from typing import Dict

from pydantic import BaseModel


class ScoreTrend(BaseModel):
    """Model Score Trends"""
    # clave: semana, valor: puntaje promedio
    weekly_average_scores: Dict[str, float]
