"""Payment Service"""
import logging
from datetime import datetime

from app.models.payment_history import PaymentHistory
from app.models.products import Products
from app.models.subscription import Subscription


class PaymentService:
    """
    Servicio de pago
    """

    def __init__(self):
        pass

    async def _suscription_from_suscription(self, event_data):
        """
        Obtiene la suscripción de la base de datos
        """
        subscription_id = event_data.get(
            "data", {}).get("object", {}).get("id")

        if subscription_id is None:
            logging.warning("No subscription found")
            return None

        found = await Subscription.find_one({"subscription_id": subscription_id})

        if found:
            logging.info("Subscription found: %s", found)
            return found

        logging.warning("No subscription found")
        return None

    async def _get_data_to_update(self, event_data):
        """
        Obtiene los datos de la suscripción
        """
        data = event_data.get("data", {}).get("object", {})

        product = await Products.find_one({"stripe_id": data.get("plan", {}).get("product", "")})
        return {
            "customer_id": data.get("customer", ""),
            "subscription_id": data.get("id", ""),
            "product_id": data.get("plan", {}).get("product", ""),
            "product_name": product.name,
            "period_start": datetime.fromtimestamp(data.get("current_period_start", 0)),
            "period_end": datetime.fromtimestamp(data.get("current_period_end", 0)),
            "event_id": data.get("id", ""),  # ID del evento
            # Fecha del evento
            "event_created_at": datetime.fromtimestamp(data.get("created", 0))
        }

    async def subscription_update(self, event_data):
        """
        Actualiza la suscripción en la base de datos
        """

        subscription = await self._suscription_from_suscription(event_data)

        if subscription is None:
            subscription = Subscription.from_subscription_event_data(
                event_data)
            product = await Products.find_one({"stripe_id": subscription.product_id})
            subscription.product_name = product.name
            await subscription.insert()
        else:

            updated_data = await self._get_data_to_update(event_data)
            for field, value in updated_data.items():
                if hasattr(subscription, field):
                    setattr(subscription, field, value)
            await subscription.save()

    async def handle_payment_succeeded(self, event_data):
        """
        Maneja el evento de pago exitoso
        """
        payment = PaymentHistory.from_event_data(event_data)
        await payment.insert()

    async def handle_subscription_delete(self, event_data):
        """
        Maneja el evento de suscripción eliminada
        """
        subscription = await self._suscription_from_suscription(event_data)

        if subscription is not None:
            await subscription.delete()
