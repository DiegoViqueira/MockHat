"""Model Authentication"""
from pydantic import BaseModel


class LoginData(BaseModel):
    """Model for storing login data."""
    username: str
    password: str
