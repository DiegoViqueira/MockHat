from pydantic import BaseModel


class ForgotPasswordRequest(BaseModel):
    """Forgot password request model."""
    email: str
