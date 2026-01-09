"""Customer"""
from app.core.settings import settings

import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException

import stripe
from starlette.requests import Request

from app.models.customer import CustomerPortalResponse, CustomerPortalRequest
from app.models.subscription import Subscription
from app.services.user_service import UserService
from app.models.stripe_plans import StripePlan, StripeSubscribePlan
# Crear el router para las rutas de clientes
router = APIRouter(prefix='/customers', tags=["Customer"])


stripe.api_key = settings.stripe.SECRET_KEY


@router.post("/portal", response_model=CustomerPortalResponse,
             responses={
                 400: {"description": "Stripe error"},
                 500: {"description": "Internal server error"},
             })
async def generate_portal_url(portal_request: CustomerPortalRequest, request: Request,
                              service=Depends(UserService)):
    """Generate a URL for the customer's billing portal in Stripe. """
    user = request.state.user
    # Obtener el customer_id de Stripe desde la base de datos
    customer = await service.get_user(str(user.id))

    try:
        # Generar la URL de sesión del portal del cliente
        session = stripe.billing_portal.Session.create(
            customer=customer.stripe_customer_id,
            return_url=portal_request.fallback_url  # URL de redirección
        )
        return CustomerPortalResponse(portal_url=session.url)
    except stripe.error.StripeError as e:
        logging.error("Stripe error: %s", e)
        raise HTTPException(
            status_code=400, detail=f"Stripe error: {e.user_message}") from e


@router.post("/subscribe-to-plan", response_model=StripeSubscribePlan,
             responses={
                 400: {"description": "Stripe error"},
                 500: {"description": "Internal server error"},
             })
async def subscribe_to_plan(plan: StripeSubscribePlan, request: Request,
                            service=Depends(UserService)):
    """Subscribe a user to a specific Stripe plan. """
    user = request.state.user
    # Obtener el customer_id de Stripe desde la base de datos
    customer = await service.get_user(str(user.id))

    # Si el usuario no tiene customer_id de Stripe, crear uno nuevo
    if customer.stripe_customer_id == '':
        stripe_customer = stripe.Customer.create(email=user.email,
                                                 name=f"{user.first_name} {user.last_name}",
                                                 metadata={"user_id": str(user.id)})
        customer.stripe_customer_id = stripe_customer['id']
        await customer.save()

    # Crear una sesión de checkout para la suscripción
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        customer=customer.stripe_customer_id,
        line_items=[
            {
                "price": plan.price_id,
                "quantity": 1,
            },
        ],
        success_url=plan.fallback_url,
        cancel_url=plan.fallback_url,
    )
    return {"checkout_url": session.url}


@router.get("/current-plan", response_model=Subscription,
            responses={
                404: {"description": "Subscription not found"},
                500: {"description": "Internal server error"},

            })
async def get_current_plan(request: Request,
                           service=Depends(UserService)):
    """
    Get the current plan of the user.
    """
    user = request.state.user
    # Obtener el customer_id de Stripe desde la base de datos
    customer = await service.get_user(str(user.id))

    if customer.stripe_customer_id != '':
        subscription = await Subscription.find_one({"customer_id": customer.stripe_customer_id})
        if subscription:
            return subscription

    raise HTTPException(status_code=404, detail="Subscription not found")


@router.get("/get-stripe-plans", response_model=List[StripePlan],
            responses={
                500: {"description": "Internal server error"},
})
async def get_stripe_plans():
    """
    Get all active plans available in Stripe.
    """
    # Obtener todos los precios activos con información del producto
    prices = stripe.Price.list(active=True, expand=["data.product"])

    # Convertir los precios a objetos StripePlan
    plans = [
        StripePlan(id=price.id,
                   name=price.product['name'],
                   product_id=price.product['id'],
                   amount=float(price.unit_amount / 100),
                   currency=price.currency,
                   interval=price.recurring["interval"] if price.recurring else None)
        for price in prices.data
        if price.active and price.product['active']
    ]
    return plans
