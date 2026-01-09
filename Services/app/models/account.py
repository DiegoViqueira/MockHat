"""Model Account"""
from datetime import datetime, UTC
from typing import List, Optional
from beanie import Document, Save, Update, before_event
from pydantic import ConfigDict, Field, BaseModel
import ulid

from app.enums.plan import Plan
from app.models.user import User


class Account(Document):
    """Modelo de documento para gestionar cuentas de usuario y sus planes asociados."""

    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    name: str = Field(...)  # Campo requerido
    plan: Plan = Field(default=Plan.FREE)
    users: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = Field(default=True)
    stripe_customer_id: Optional[str] = Field(
        default='', description="Stripe customer ID")

    class Settings:
        """Configuración de la colección de cuentas."""
        name = "accounts"
        indexes = [
            [("id", 1)],
        ]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @before_event(Save, Update)
    async def set_updated_at(self):
        """Set the updated_at field to the current UTC time"""
        self.updated_at = datetime.now(UTC)


class AccountDto(BaseModel):
    """Modelo de documento para gestionar cuentas de usuario y sus planes asociados."""
    id: str
    name: str
    plan: Plan
    users: Optional[List[User]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    is_active: bool = Field(default=True)
