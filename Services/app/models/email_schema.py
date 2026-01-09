"""Model Email Schema"""
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    """Model for storing email information."""
    name: str
    email: EmailStr
    subject: str
    message: str
    recaptchaToken: str  # Token de reCAPTCHA
