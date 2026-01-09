"""Model Class Metrics"""

from typing import List
from pydantic import BaseModel, Field


from app.models.metrics.score_histogram import ScoreHistogram
from app.models.metrics.score_trends import ScoreTrend
from app.models.metrics.class_score_metrics import ClassScoreMetrics
from app.models.metrics.student_metrics import StudentMetrics
from app.models.metrics.criteria_average import CriteriaAverage


class ClassMetrics(BaseModel):
    """Model Class Metrics"""
    score_histogram: ScoreHistogram = Field(default=None,
                                            description="Histograma de puntajes")
    score_trends: ScoreTrend = Field(
        default=None, description="Tendencias de puntajes")
    criteria_average: CriteriaAverage = Field(
        default=None, description="Puntajes promedio por criterio")
    class_score_metrics: ClassScoreMetrics = Field(
        default=None, description="Métricas agregadas por clase")
    student_metrics: List[StudentMetrics] = Field(
        default=None, description="Métricas agregadas por estudiante")
