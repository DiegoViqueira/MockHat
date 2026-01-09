"""Auth Service"""
from datetime import timedelta, datetime, timezone
from typing import List

from fastapi import Depends, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext
from jose import jwt
from google.oauth2 import id_token
from google.auth.transport import requests


from app.core.settings import settings
from app.enums.role import Role
from app.models.token import Token
from app.services.user_service import UserService


class AuthService:
    """Auth service"""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/auth/login", scheme_name="Bearer", auto_error=False)

    @staticmethod
    def required_auth(allowed_roles: List[Role]):
        """
        Decorator to check if the user has the required role.
        """
        def role_checker(current_role: Role = Depends(AuthService.get_token_role)):

            if current_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Role not authorized"
                )

        return role_checker

    @staticmethod
    def get_token_role(token: str = Depends(oauth2_scheme)) -> Role:
        """
        Get the role of the user from the token.
        """
        payload = AuthService.decode_token(token)
        user_role = payload.get("role")
        if user_role:
            return Role[user_role]  # Convert string to Role enum

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Role not found in token"
        )

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """
        Verify the password of the user.
        """
        return AuthService.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    async def authenticate_user(email: str, password: str):
        """
        Authenticate the user.
        """
        user = await UserService.get_user_by_email(email)
        if not user or user.disabled or not AuthService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    async def create_verify_register_token(user_id: str, account_id: str):
        """
        Create the verify register token for the user.
        """
        return jwt.encode({"sub": user_id, "account_id": account_id}, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)

    @staticmethod
    async def verify_register_token(token: str):
        """
        Verify the register token.
        """
        try:
            decoded_token = jwt.decode(
                token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
            user_id = decoded_token.get("sub")
            account_id = decoded_token.get("account_id")
            user = await UserService.get_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )
            if user.account_id != account_id:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )
            user.verified = True
            await user.save()

        except Exception as exc:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            ) from exc

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        """
        Create the access token for the user.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + \
            (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        """
        Decode the token.
        """
        try:
            return jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
        except Exception as exc:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            ) from exc

    @staticmethod
    def validate_token(scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
        """
        Validate the token.
        """
        payload = AuthService.decode_token(token)
        token_scopes = payload.get("scopes", [])
        required_scopes = scopes.scopes

        if not any(scope in token_scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload

    @staticmethod
    def validate_google_token(token: str, client_id: str):
        """
        Validate the Google token.
        """
        try:
            id_info = id_token.verify_oauth2_token(
                token, requests.Request(), client_id)
            return id_info
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google ID token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

    @staticmethod
    async def get_websocket_token(websocket: WebSocket):
        """
        Get the websocket token.
        """
        await websocket.accept()
        return await websocket.receive_text()

    @staticmethod
    async def validate_websocket_token(token: str = Depends(get_websocket_token)):
        """
        Validate the websocket token.
        """
        return jwt.decode(token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])

    @staticmethod
    def generate_app_token(user):
        """Generate access and refresh tokens for a user."""

        access_token_expires = timedelta(
            minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(
            days=settings.auth.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = AuthService.create_access_token(
            data={"sub": user.email, "role": user.role.value, "id": str(
                user.id), "account_id": str(user.account_id)},
            expires_delta=access_token_expires,
        )
        refresh_token = AuthService.create_access_token(
            data={"sub": user.email, "role": user.role.value, "id": str(
                user.id), "account_id": str(user.account_id)},
            expires_delta=refresh_token_expires,
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES,
            token_type="bearer",
        )

    @staticmethod
    async def create_forgot_password_token(user_id: str, account_id: str):
        """
        Create the forgot password token for the user.
        """
        return jwt.encode({"sub": user_id, "account_id": account_id}, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)

    @staticmethod
    async def create_invite_user_to_account_token(user_id: str, email: str, account_name: str, account_id: str, role: Role):
        """
        Create the invite user to account token for the user.
        """
        return jwt.encode({"sub": user_id, "email": email, "account_name": account_name, "account_id": account_id, "role": role.value}, settings.auth.SECRET_KEY, algorithm=settings.auth.ALGORITHM)

    @staticmethod
    async def verify_invite_user_to_account_token(token: str):
        """
        Verify the invite user to account token.
        """
        try:
            decoded_token = jwt.decode(
                token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
            user_id = decoded_token.get("sub")
            account_id = decoded_token.get("account_id")
            role = decoded_token.get("role")
            email = decoded_token.get("email")
            user = await UserService.get_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )
            if user.account_id != account_id:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )

            return user, email, account_id, role
        except Exception as exc:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            ) from exc

    @staticmethod
    async def verify_forgot_password_token(token: str):
        """
        Verify the forgot password token.
        """
        try:
            decoded_token = jwt.decode(
                token, settings.auth.SECRET_KEY, algorithms=[settings.auth.ALGORITHM])
            user_id = decoded_token.get("sub")
            account_id = decoded_token.get("account_id")
            user = await UserService.get_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )
            if user.account_id != account_id:
                raise HTTPException(
                    status_code=403, detail="Could not validate credentials"
                )
            return user
        except Exception as exc:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            ) from exc
