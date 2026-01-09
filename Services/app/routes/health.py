"""Health"""
from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_class=Response, summary="Ping the server",
            description="Pings the server to check if it is running.",
            status_code=200)
async def ping():
    """Ping the server to check if it is running."""
    return Response(content="", media_type="application/json")
