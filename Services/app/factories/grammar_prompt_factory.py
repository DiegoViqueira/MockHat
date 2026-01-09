"""GrammarPromptFactory"""
from app.enums.level import Level


class GrammarExtraPromptFactory:
    """
    This factory is used to create a prompt for the writing transcription task.
    """

    def __init__(self):
        self.mapping = {
            Level.A1: """
                Do **not** identify as grammar errors:
                - missing punctuation.
            """,
            Level.A2: """
                Do **not** identify as grammar errors:
                - missing punctuation.
            """,
            Level.B1: """
                Do **not** identify as grammar errors:
                - Uppercase letters at the beginning of the sentence.
                - Lowercase letters at the beginning of the sentence.
                - Missing commas.
                - missing punctuation.
                """,
            Level.B2: """
                Do **not** identify as grammar errors:
                - Uppercase letters at the beginning of the sentence.
                - Lowercase letters at the beginning of the sentence.
                - missing punctuation.
            """,
            Level.C1: """
                Do **not** identify as grammar errors:
                - Uppercase letters at the beginning of the sentence.
                - Lowercase letters at the beginning of the sentence.
                - missing punctuation.
            """,
            Level.C2: """
                Do **not** identify as grammar errors:
                - Uppercase letters at the beginning of the sentence.
                - Lowercase letters at the beginning of the sentence.
                - missing punctuation.
            """,
            Level.EBAU: """
                Do **not** identify as grammar errors:
                - Uppercase letters at the beginning of the sentence.
                - Lowercase letters at the beginning of the sentence.
                - missing punctuation.
            """
        }

    def get(self, level: Level) -> str | None:
        """
        Get the prompt for the writing transcription task.
        """
        return self.mapping.get(level)
