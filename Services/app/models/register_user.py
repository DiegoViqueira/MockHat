"""Model Register User"""
from typing import Optional
from pydantic import BaseModel, Field


class RegisterUser(BaseModel):
    """Register user model"""
    account_name: str = Field(...)
    email: str = Field(...)
    first_name: str = Field('')
    last_name: str = Field('')
    password: str = Field(...)
    token: Optional[str] = Field(default=None)
    terms_and_conditions_accepted: Optional[bool] = Field(default=False)
