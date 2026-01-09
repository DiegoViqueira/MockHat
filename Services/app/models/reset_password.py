

from pydantic import BaseModel


class ResetPasswordRequest(BaseModel):
    """Reset password request model."""
    token: str
    password: str
