"""Payments"""
import logging

from fastapi import APIRouter, HTTPException, status, Query
from starlette.requests import Request

from app.models.user import User
from app.models.payment_history import PaymentHistory, PaymentHistoryListResult


router = APIRouter(prefix='/payments', tags=["Payments"])


@router.get("", response_model=PaymentHistoryListResult,
            responses={
                500: {"description": "Internal server error"},
            })
async def search_payments(request: Request, limit: int = Query(10, alias="limit"),
                          skip: int = Query(0, alias="offset")):
    """Search payments."""
    user = await User.get(request.state.user.id)

    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        payments = await PaymentHistory.find({"customer_email": user.email}).sort("-_id").skip(skip).limit(limit).to_list(limit)
        total_count = await PaymentHistory.find({"customer_email": user.email}).count()

        result = PaymentHistoryListResult(payments=payments, total=total_count)
        return result

    except Exception as e:
        logging.error("Error list Payments from database: %s", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error saving updated writing to database.") from e
