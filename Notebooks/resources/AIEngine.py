from abc import ABC


class AIEngine(ABC):
    def __init__(self):
        self.client = None
