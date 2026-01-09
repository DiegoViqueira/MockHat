"""Payments"""
from contextlib import asynccontextmanager

import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.api_config_payments import fastAPI_Options
from app.core.settings import settings
from app.events.lifespan import init_db
from app.handlers.exception_handlers import api_exception_handler
from app.loggers.loggers import LOGGING_CONFIG
from app.routes.health import router as health_router
from app.routes.payments_webhook import router as webhooks_router


stripe.api_key = settings.stripe.SECRET_KEY

# Specify allowed origins
allow_origins = [
    "http://localhost:4200",  # For development
    "https://api.mockhat.com"  # For production
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Vida útil de la aplicación
    """
    await init_db()
    yield

app = FastAPI(**fastAPI_Options, lifespan=lifespan)

app.include_router(health_router)
app.include_router(webhooks_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_exception_handler(Exception, api_exception_handler)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.payments:app", host="0.0.0.0", port=8000,
                reload=True, log_config=LOGGING_CONFIG)
