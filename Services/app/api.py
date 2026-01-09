"""API"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.handlers.http_exception_handler import http_exception_handler
from app.loggers.loggers import LOGGING_CONFIG
from app.middlewares.auth_middleware import AuthMiddleware
from app.routes.users import router as users_route
from app.routes.auth import router as auth_router
from app.handlers.exception_handlers import api_exception_handler
from app.routes.health import router as health_router
from app.routes.students import router as student_route
from app.routes.contact import router as contact_route
from app.routes.payments import router as payments_route
from app.routes.customer import router as customer_route
from app.routes.classes import router as class_route
from app.routes.accounts import router as account_route
from app.routes.assessments import router as assessment_route
from app.core import api_config_api
from app.events.lifespan import init_db, init_db_admin_user
from starlette.exceptions import HTTPException as StarletteHTTPException


origins = ["*"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan event."""
    await init_db()
    await init_db_admin_user()
    yield

app = FastAPI(**api_config_api.fastAPI_Options, lifespan=lifespan)


app.include_router(account_route)
app.include_router(assessment_route)
app.include_router(auth_router)
app.include_router(class_route)
app.include_router(contact_route)
app.include_router(customer_route)
app.include_router(health_router)
app.include_router(payments_route)
app.include_router(student_route)
app.include_router(users_route)


app.add_middleware(BaseHTTPMiddleware, dispatch=AuthMiddleware())


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
_ = APIKeyHeader(name="Authorization", auto_error=False)


app.add_exception_handler(Exception, api_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000,
                reload=True, log_config=LOGGING_CONFIG)
