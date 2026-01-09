"""FewShotWritingDB"""
import os
import json
import logging
from typing import Dict, Tuple, Optional, Any
from functools import lru_cache

from app.enums.level import Level
from app.enums.institution import Institution
from app.enums.writing_task import WritingTask
from app.core.interfases.singleton_meta import SingletonMeta


class FewShotWritingDB(metaclass=SingletonMeta):
    """
    Singleton class to manage few-shot writing example references
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
        """Get the default data directory relative to this file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "data", "few_shots")

    def _load_database(self) -> Dict[Tuple[Institution, Level, WritingTask], str]:
        """
        Load JSON few-shot files into the database.
        Returns a dictionary mapping (Institution, Level, Task) to file paths.
        """
        db = {}
        for institution in Institution:
            for level in Level:
                for task in WritingTask:
                    filename = f"{institution.value.upper()}_{level.value.upper()}_{task.value}.json"
                    filepath = os.path.join(self.data_dir, filename)
                    if os.path.exists(filepath):
                        db[(institution, level, task)] = filepath
        return db

    @property
    def db(self) -> Dict[Tuple[Institution, Level, WritingTask], str]:
        """
        Get the database of few-shot writing examples.
        """
        if self._db is None:
            self._db = self._load_database()
        return self._db

    @lru_cache(maxsize=128)
    def _read_file(self, filepath: str) -> Optional[Dict[str, Any]]:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logging.error("Error loading few-shot file %s: %s", filepath, e)
            return None

    def get_few_shot_writing(
        self,
        institution: Institution,
        level: Level,
        task: WritingTask
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve the few-shot writing example for the given institution, level, and task.
        Returns None if not found.
        """
        path = self.db.get((institution, level, task))
        return self._read_file(path) if path else None
