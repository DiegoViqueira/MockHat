"""Payments Webhook"""
import logging
import stripe

from fastapi import APIRouter, HTTPException, Depends
from starlette.requests import Request

from app.services.payment_service import PaymentService
from app.services.product_service import ProductService
from app.core.settings import settings

router = APIRouter(prefix='/webhook', tags=["Webhooks"])


@router.post("")
async def stripe_webhook(request: Request, payment_service=Depends(PaymentService),
                         products_services=Depends(ProductService)):
    """
    Webhook de Stripe
    """
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe.SIGNING_SECRET_DE_WEBHOOK
        )

    except stripe.error.SignatureVerificationError as e:
        logging.error("Firma de Webhook no válida: %s", e)
        raise HTTPException(
            status_code=400, detail="Firma de Webhook no válida")

    logging.info(event['type'])

    if event['type'] == 'invoice.payment_succeeded':
        await payment_service.handle_payment_succeeded(event)

    elif event['type'] == 'customer.subscription.deleted':
        logging.info("Customer subscription Deleted")
        await payment_service.handle_subscription_delete(event)

    elif event['type'] == 'customer.subscription.created':
        logging.info("Customer suscription Created :")
        await payment_service.subscription_update(event)

    elif event['type'] == 'customer.subscription.updated':
        logging.info("Update de suscripción exitoso para:")
        await payment_service.subscription_update(event)

    elif event['type'] == 'invoice.payment_failed':
        logging.error("Pago de suscripción fallido para:", )

    elif event['type'] == 'product.created':
        logging.info("Nuevo producto creado.")
        await products_services.create_or_update_product(event)

    elif event['type'] == 'product.updated':
        logging.info("Producto actualizado.")
        await products_services.create_or_update_product(event)

    return {"status": "success"}
