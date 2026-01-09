from datetime import UTC, datetime
from app.models.writing import Writing


class AccountTransactionQuotaManager:
    """
    Manage the account transaction quota
    """

    @staticmethod
    async def get_account_transaction_usage(account_id: str) -> int:
        """
        Get the account transaction usage
        """

        # Obtener el primer día del mes actual
        first_day_of_month = datetime.now(UTC).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

        query = {
            "account_id": account_id,
            "created_at": {"$gte": first_day_of_month}
        }
        total = await Writing.find(query).count()

        return total
