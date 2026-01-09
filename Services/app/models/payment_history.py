"""Model Payment History"""
from typing import List

from beanie import Document
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, UTC
import ulid


class PaymentHistory(Document):
    """Model for storing payment history information."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    # Información del cliente
    customer_id: str = Field("", description="ID del cliente en Stripe")
    customer_email: EmailStr = Field(
        "", description="Correo electrónico del cliente")

    # Información de la suscripción
    subscription_id: str = Field(
        "", description="ID de la suscripción en Stripe")
    plan_description: str = Field(
        "", description="Descripción del plan contratado")
    period_start: datetime = Field(
        "", description="Inicio del ciclo de facturación")
    period_end: datetime = Field(...,
                                 description="Fin del ciclo de facturación")

    # Información de la factura
    invoice_id: str = Field("", description="ID de la factura en Stripe")
    payment_status: str = Field("", description="Estado del pago")
    amount_paid: int = Field("", description="Monto pagado en centavos")
    currency: str = Field("", description="Moneda de la factura")
    invoice_pdf_url: str = Field("", description="URL del PDF de la factura")

    # Información del evento de webhook
    event_id: str = Field("", description="ID del evento de webhook en Stripe")
    event_created_at: datetime = Field(
        "", description="Fecha de creación del evento")

    # Fechas de auditoría
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Fecha de creación en la base de datos")

    class Settings:
        name = "payment_history"
        collection = "payment_history"
        indexes = [
            "customer_email"
        ]


class PaymentHistoryListResult(BaseModel):
    """Result for listing payment history."""
    payments: List[PaymentHistory] = Field(default=[])
    total: int = Field(default=0)
