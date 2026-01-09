"""Auth Middleware"""
import logging

from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.services.auth_service import AuthService
from app.services.user_service import UserService


class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware para la autenticación de usuarios."""

    def __init__(self):
        """Inicializa el middleware."""
        self.user_service = UserService()

    async def __call__(self, request: Request, call_next, **kwargs):
        paths_to_skip = ["/health", "/contact/send-email", "/auth/login-form", "/auth/login",
                         "/docs", "/openapi.json", "/auth/google", "/auth/microsoft", "/auth/signup", "/auth/verify-register", "/auth/reset-password", "/auth/forgot-password",
                         ]

        if not any(path in request.url.path for path in paths_to_skip):
            logging.info("AuthMiddleware called for path: %s",
                         request.url.path)
            authorization: str = request.headers.get("Authorization")
            user = None

            if authorization:
                try:
                    token_type, token = authorization.split(" ")
                    if token_type.lower() == "bearer":
                        payload = AuthService.decode_token(token)
                        user_id = payload.get("id")
                        user = await UserService.get_user(user_id)
                        if not user:
                            raise HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="User not found",
                                headers={"WWW-Authenticate": "Bearer"},
                            )
                    else:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token type",
                            headers={"WWW-Authenticate": "Bearer"},
                        )

                except HTTPException as auth_exc:
                    # Pass on specific HTTPException raised during token validation
                    raise auth_exc
                except Exception as e:
                    logging.error("Token validation error: %s", e)
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token validation failed",
                        headers={"WWW-Authenticate": "Bearer"},
                    ) from e
            else:
                logging.warning("Missing Authorization header")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header missing",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            request.state.user = user
        else:
            logging.info("AuthMiddleware skipped for path: %s",
                         request.url.path)

        return await call_next(request)
