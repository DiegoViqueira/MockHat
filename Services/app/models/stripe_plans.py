"""Model Stripe Plans"""
from pydantic import BaseModel, Field


class StripePlan(BaseModel):
    """
    Modelo que representa un plan de suscripción en Stripe.
    """
    id: str = Field(
        '',
        description="Identificador único del precio en Stripe"
    )
    product_id: str = Field(
        '',
        description="Identificador único del producto asociado en Stripe"
    )
    name: str = Field(
        '',
        description="Nombre del plan de suscripción"
    )
    amount: float = Field(
        default=0,
        description="Precio del plan en la moneda especificada"
    )
    currency: str = Field(
        '',
        description="Código de la moneda (ejemplo: 'usd', 'eur')"
    )
    interval: str = Field(
        '',
        description="Intervalo de facturación ('month', 'year', etc.)"
    )


class StripeSubscribePlan(BaseModel):
    """
    Modelo para la solicitud de suscripción a un plan.
    """
    price_id: str = Field(
        '',
        description="Identificador del precio del plan en Stripe"
    )
    fallback_url: str = Field(
        '',
        description="URL de retorno después de completar o cancelar la suscripción"
    )
