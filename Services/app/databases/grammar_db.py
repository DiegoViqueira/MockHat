"""GrammarDB"""
import os
import logging
from typing import Dict, Tuple, Optional
from functools import lru_cache

from app.core.interfases.singleton_meta import SingletonMeta
from app.enums.institution import Institution
from app.enums.level import Level


class GrammarDB(metaclass=SingletonMeta):
    """
    Singleton class to manage grammar markdown references
    by institution and level.
    """

    def __init__(self, data_dir: Optional[str] = None):
        # Ensure the initialization runs only once
        if getattr(self, "_initialized", False):
            return

        self.data_dir = data_dir or self._default_data_dir()
        os.makedirs(self.data_dir, exist_ok=True)

        self._db: Optional[Dict[Tuple[Institution, Level], str]] = None
        self._initialized = True

    def _default_data_dir(self) -> str:
        """Get the default data directory relative to this file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_dir, "data", "grammar")

    def _load_database(self) -> Dict[Tuple[Institution, Level], str]:
        """
        Load markdown files into the database mapping.
        Returns a dictionary mapping (Institution, Level) to file paths.
        """
        db = {}
        for institution in Institution:
            for level in Level:
                filename = f"{institution.value.upper()}_{level.value.upper()}.md"
                filepath = os.path.join(self.data_dir, filename)
                if os.path.exists(filepath):
                    db[(institution, level)] = filepath
        return db

    @property
    def db(self) -> Dict[Tuple[Institution, Level], str]:
        """Lazy-loaded property for accessing the file path map."""
        if self._db is None:
            self._db = self._load_database()
        return self._db

    @lru_cache(maxsize=128)
    def _read_file(self, filepath: str) -> Optional[str]:
        """Read and return the contents of a grammar file (cached)."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError as e:
            logging.error("Error loading grammar file %s: %s", filepath, e)
            return None

    def get_grammar(self, institution: Institution, level: Level) -> Optional[str]:
        """
        Retrieve the grammar reference markdown text for the given institution and level.
        Returns None if not found.
        """
        path = self.db.get((institution, level))
        return self._read_file(path) if path else None
