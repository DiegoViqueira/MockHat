"""Service for writing analytics"""
from collections import defaultdict
from statistics import mean
from typing import List
import numpy as np
import pandas as pd
import logging

from app.enums.writing_state import WritingState
from app.models.classes import Class
from app.models.metrics.student_metrics import ScoreEntry, StudentMetrics, AssessmentMetrics, AssessmentsMetrics
from app.models.writing import Writing
from app.models.metrics.class_score_metrics import ClassScoreMetrics
from app.models.metrics.score_histogram import ScoreHistogram
from app.models.metrics.score_trends import ScoreTrend
from app.models.metrics.criteria_average import CriteriaAverage
from app.factories.pass_rate_factory import PassRateFactory


class WritingAnalyticsService:
    """Service for writing analytics"""
    @staticmethod
    async def get_class_score_metrics(class_id: str) -> ClassScoreMetrics:
        """
        Métricas agregadas por clase:
        - Puntaje promedio
        - Desviación estándar de puntajes
        - Porcentaje de aprobados (score >= 60)
        - Promedio de errores gramaticales
        """

        writings = await Writing.find({"class_id": class_id, "writing_state": WritingState.COMPLETED}).to_list()

        if not writings:
            return ClassScoreMetrics(
                average_score=0.0,
                pass_rate=0.0,
                avg_grammar_errors=0.0
            )

        pass_rate_factory = PassRateFactory()
        pass_rate = pass_rate_factory.get_pass_rate(
            writings[0].institution, writings[0].exam_type, writings[0].level)

        scores = [sum(c.score for c in w.ai_feedback.criterias)
                  for w in writings]
        grammar_errors = [
            len(w.grammar_feedback.errors) for w in writings
        ]

        passed_count = len([s for s in scores if s >= pass_rate])

        class_score_metrics = ClassScoreMetrics(
            average_score=round(mean(scores), 0) if scores else 0.0,
            pass_rate=(passed_count / len(scores)) * 100 if scores else 0.0,
            avg_grammar_errors=round(
                mean(grammar_errors), 0) if grammar_errors else 0.0,
        )

        return class_score_metrics

    @staticmethod
    async def get_score_trend_over_time(class_id: str) -> ScoreTrend:
        """
        Evolution of the performance over time:
        - Trend of the average score per week
        """
        writings = await Writing.find({"class_id": class_id, "writing_state": WritingState.COMPLETED}).to_list()

        if not writings:
            return ScoreTrend(weekly_average_scores={})

        # Crear un DataFrame con los datos relevantes
        data = [{
            "created_at": w.created_at,
            "writing_score": sum(c.score for c in w.ai_feedback.criterias)
        } for w in writings]

        df = pd.DataFrame(data)

        # Asegurarse de que 'created_at' sea de tipo datetime
        df["created_at"] = pd.to_datetime(df["created_at"])

        # Establecer 'created_at' como índice
        df.set_index("created_at", inplace=True)

        # Agrupar por semana y calcular la media, reemplazando NaN por 0.0
        weekly_avg = df.resample("W")["writing_score"].mean().dropna()

        # Convertir los resultados a un diccionario con formato de fecha
        weekly_average_scores = {
            week.strftime("%Y-%m-%d"): round(score, 2) for week, score in weekly_avg.items()
        }

        return ScoreTrend(weekly_average_scores=weekly_average_scores)

    @staticmethod
    async def get_criteria_average(class_id: str) -> CriteriaAverage:
        """
        Analysis by evaluation criteria:
        - Average score per criteria
        """
        writings = await Writing.find({"class_id": class_id, "writing_state": WritingState.COMPLETED}).to_list()

        if not writings:
            return CriteriaAverage(criteria_scores={})

        criteria_scores_raw = {}

        for w in writings:
            for c in w.ai_feedback.criterias:
                crit = c.criteria
                criteria_scores_raw.setdefault(crit, []).append(c.score)

        # Calculate the average for each criteria
        criteria_scores_avg = {
            crit: mean(scores) for crit, scores in criteria_scores_raw.items()
        }

        return CriteriaAverage(criteria_scores=criteria_scores_avg)

    @staticmethod
    async def get_score_histogram(class_id: str, bins: int = 10) -> ScoreHistogram:
        """
        Histograma de puntajes:
        - Devuelve frecuencia por intervalos
        """
        writings = await Writing.find({"class_id": class_id, "writing_state": WritingState.COMPLETED}).to_list()

        if not writings:
            return ScoreHistogram(histogram=[], bin_edges=[])

        valid_scores = [
            sum(c.score for c in w.ai_feedback.criterias) /
            len(w.ai_feedback.criterias)
            for w in writings
            if w.ai_feedback and w.ai_feedback.criterias  # <-- asegura que haya criterios
            # <-- asegura que fue evaluado correctamente
            and w.writing_state == WritingState.COMPLETED
        ]
        hist, bin_edges = np.histogram(valid_scores, bins=bins)

        score_histogram = ScoreHistogram(
            histogram=hist.tolist(),
            bin_edges=bin_edges.tolist()
        )

        return score_histogram

    @staticmethod
    async def get_student_metrics(class_id: str) -> List[StudentMetrics]:
        """
           Metrics by student:
           - Average score per criterion
        """
        logging.info("Getting student metrics for class %s", class_id)
        class_ = await Class.get(class_id)

        if not class_:
            return []

        student_metrics_list = []

        for student in class_.students:
            logging.info(
                "Getting student metrics for student %s", student.name)
            # Writings completados por estudiante
            student_writings = await Writing.find({
                "student_id": student.id,
                "class_id": class_id,
                "writing_state": WritingState.COMPLETED
            }).to_list()

            if not student_writings:
                logging.info(
                    "No writings found for student %s", student.name)
                student_metrics_list.append(StudentMetrics(
                    name=student.name + " " + student.last_name,

                ))
                continue

            assessment_list = []
            total_score = 0
            pass_rate_factory = PassRateFactory()
            pass_rate = pass_rate_factory.get_pass_rate(
                student_writings[0].institution, student_writings[0].exam_type, student_writings[0].level)

            for writing in student_writings:
                score_entries = [
                    ScoreEntry(criteria=cs.criteria, score=cs.score)
                    for cs in writing.ai_feedback.criterias
                ]
                total_score += sum(se.score for se in score_entries)
                assessment = AssessmentMetrics(
                    date=writing.created_at.date().isoformat(),
                    scores=score_entries,
                    grammar_errors=len(writing.grammar_feedback.errors)
                )
                assessment_list.append(assessment)

            avg_grammar_errors = round(sum(
                assessment.grammar_errors for assessment in assessment_list) / len(assessment_list), 0)
            student_metrics = StudentMetrics(
                name=student.name + " " + student.last_name,
                assessments=AssessmentsMetrics(
                    assessments=assessment_list,
                    count=len(assessment_list),
                    score_average=round(total_score / len(assessment_list), 0),
                    grammar_errors_average=avg_grammar_errors,
                    pass_rate=pass_rate
                )
            )
            student_metrics_list.append(student_metrics)

        return student_metrics_list
