"""RubricDB"""
import os
import logging
from typing import Dict, Tuple, Optional
from functools import lru_cache

from app.enums.institution import Institution
from app.enums.level import Level
from app.enums.writing_task import WritingTask
from app.core.interfases.singleton_meta import SingletonMeta


class RubricDB(metaclass=SingletonMeta):
    """
    Singleton class to manage rubric markdown references
    by institution, level, and writing task.
    """

    def __init__(self, data_dir: Optional[str] = None):
        if getattr(self, "_initialized", False):
            return

        self.data_dir = data_dir or self._default_data_dir()
        os.makedirs(self.data_dir, exist_ok=True)

        self._db: Optional[Dict[Tuple[Institution,
                                      Level, WritingTask], str]] = None
        self._initialized = True

    def _default_data_dir(self) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "data", "rubrics")

    def _load_database(self) -> Dict[Tuple[Institution, Level, WritingTask], str]:
        """
        Load markdown rubric files into the database.
        Returns a dictionary mapping (Institution, Level, Task) to file paths.
        """
        db = {}
        for institution in Institution:
            for level in Level:
                for task in WritingTask:
                    filename = f"{institution.value.upper()}_{level.value.upper()}_{task.value}.md"
                    filepath = os.path.join(self.data_dir, filename)
                    if os.path.exists(filepath):
                        db[(institution, level, task)] = filepath
        return db

    @property
    def db(self) -> Dict[Tuple[Institution, Level, WritingTask], str]:
        """
        Get the database of rubric references.
        """
        if self._db is None:
            self._db = self._load_database()
        return self._db

    @lru_cache(maxsize=128)
    def _read_file(self, filepath: str) -> Optional[str]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            logging.error("Error loading rubric file %s: %s", filepath, e)
            return None

    def get_rubric(self, institution: Institution, level: Level, task: WritingTask) -> Optional[str]:
        """
        Retrieve the rubric markdown text for the given institution, level, and task.
        Returns None if not found.
        """
        path = self.db.get((institution, level, task))
        return self._read_file(path) if path else None
