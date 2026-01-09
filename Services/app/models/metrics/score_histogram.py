"""Model Score Histogram"""
from typing import List

from pydantic import BaseModel


class ScoreHistogram(BaseModel):
    """Model Score Histogram"""
    # Frecuencia de puntajes en cada bin
    histogram: List[int]
    # Límites de los bins
    bin_edges: List[float]
