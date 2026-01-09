"""Model Token"""
from pydantic import BaseModel


class Token(BaseModel):
    """Model for storing token information."""
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str


class TokenData(BaseModel):
    """Model for storing token data."""
    email: str | None = None
    scopes: list[str] | None = None


class TokenRequest(BaseModel):
    """Model for storing token request."""
    token: str
