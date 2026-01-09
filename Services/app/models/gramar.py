"""Model Grammar"""
from pydantic import BaseModel, Field

from app.models.grammar_error import GrammarError


class Grammar(BaseModel):
    """Grammar model."""
    errors: list[GrammarError] = Field(
        default=[], description="The list of grammar errors.")


class GammarAi(BaseModel):
    """Gammar AI model."""
    errors: list[GrammarError] = Field(
        description="The list of grammar errors.")

    def __str__(self) -> str:
        return self.to_string()

    def to_string(self) -> str:
        """
        Convert the grammar errors to a string.
        """
        if not self.errors:
            return "No se encontraron errores gramaticales."

        result = "# Errores Gramaticales\n\n"
        for i, error in enumerate(self.errors, 1):
            result += f"## Error {i}\n"
            result += f"**Texto original:** {error.error_text}\n\n"
            result += f"**Corrección:** {error.corrected_text}\n\n"
            result += f"**Explicación:** {error.correction_explanation}\n\n"
            result += "---\n\n"

        return result
