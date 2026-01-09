"""GrammarReferenceFactory"""
import logging
from app.databases.grammar_db import GrammarDB
from app.enums.institution import Institution
from app.enums.level import Level


class GrammarReferenceFactory:
    """
    This factory is used to create a grammar reference for the given institution and level.
    """

    def __init__(self):
        self.grammar_db = GrammarDB()

    def get_grammar_reference(self, institution: Institution, level: Level) -> str:
        """
        Get the grammar reference for the given institution and level.
        """
        grammar = self.grammar_db.get_grammar(institution, level)
        if grammar is None:
            logging.warning("!!!!!!!!!!!!!!!!!!!!!Grammar reference is empty")
            return ""
        return grammar
