"""Model Subscription"""
from typing import List

from beanie import Document
from pydantic import BaseModel, Field
from datetime import datetime, UTC
import ulid


class Subscription(Document):
    """Model for storing subscription information."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    customer_id: str = Field("", description="ID del cliente en Stripe")
    subscription_id: str = Field(
        "", description="ID de la suscripción en Stripe")
    product_id: str = Field("", description="ID del producto.")
    product_name: str = Field("", description="Nombre del producto")
    period_start: datetime = Field(
        "", description="Inicio del ciclo de facturación")
    period_end: datetime = Field(...,
                                 description="Fin del ciclo de facturación")
    event_id: str = Field("", description="ID del evento de webhook en Stripe")
    event_created_at: datetime = Field(
        "", description="Fecha de creación del evento")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Fecha de creación en la base de datos")

    class Settings:
        """Settings for the subscriptions collection."""
        name = "subscriptions"
        collection = "subscriptions"

        indexes = [
            "customer_id",
            "subscription_id"
        ]


class SubscriptionListResult(BaseModel):
    """Result for listing subscriptions."""
    subscriptions: List[Subscription] = Field(default=[])
    total: int = Field(default=0)
