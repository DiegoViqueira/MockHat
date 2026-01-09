""" pass_rate_factory """

from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.exam_type import ExamType
import logging


class PassRateFactory:
    """
    This factory is used to get the pass rate for the given institution, exam type and level.
    """

    def __init__(self):
        self.pass_rate_db = {
            (Institution.CAMBRIDGE, ExamType.CEQ): {
                Level.A1: 10,
                Level.A2: 10,
                Level.B1: 10,
                Level.B2: 10,
                Level.C1: 10,
                Level.C2: 10,
            },
            (Institution.BACHILLERATO, ExamType.EBAU): {
                Level.EBAU: 80
            }
        }

    def get_pass_rate(self, institution: Institution, exam_type: ExamType, level: Level) -> int:
        """
        Get the pass rate for the given institution, exam type and level.
        """
        try:
            pass_rate = self.pass_rate_db[(institution, exam_type)][level]
            return pass_rate
        except KeyError:
            logging.error("No pass rate defined for %s, %s, %s",
                          institution, exam_type, level)
            return 0
