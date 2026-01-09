from datetime import datetime, UTC
from typing import List
import ulid
from pydantic import BaseModel, EmailStr, Field
from beanie import Document
from pymongo import IndexModel
from app.enums.role import Role


class AccountInvitation(Document):
    """Modelo de documento para gestionar invitaciones a cuentas."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    account_id: str = Field(...)
    email: EmailStr = Field(...)
    role: Role = Field(default=Role.MEMBER)
    token: str = Field(...)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class Settings:
        """Configuración de la colección de cuentas."""
        name = "account_invitations"
        indexes = [
            IndexModel(
                [("account_id", 1), ("email", 1)],
                unique=True
            ),
            [
                ("account_id", 1),
            ],

        ]


class ListInvitations(BaseModel):
    """List of invitations"""
    invitations: List[AccountInvitation]
    total: int
