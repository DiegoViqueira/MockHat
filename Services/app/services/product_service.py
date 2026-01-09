"""Product Service"""
from app.models.products import Products


class ProductService:
    """
    Servicio de productos
    """

    def __init__(self):
        pass

    async def create_or_update_product(self, event_data):
        """
        Crea o actualiza un producto en la base de datos
        """
        product_id = event_data.get("data", {}).get("object", {}).get("id")

        if not product_id:
            return False

        found = await Products.find_one({"stripe_id": product_id})

        if found is None:
            new_product = Products(name=event_data.get("data", {}).get("object", {}).get("name"),
                                   metadata=event_data.get("data", {}).get(
                                       "object", {}).get("metadata"),
                                   stripe_id=product_id)
            await Products.insert_one(new_product)
        else:
            found.metadata = event_data.get("data", {}).get(
                "object", {}).get("metadata")
            await found.save()

        return True
