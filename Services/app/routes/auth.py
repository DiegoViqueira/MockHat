"""Auth"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.models.account_invitations import AccountInvitation
from app.models.forgot_password import ForgotPasswordRequest
from app.models.reset_password import ResetPasswordRequest
from app.services.auth_service import AuthService
from app.enums.role import Role
from app.models.token import Token
from app.models.user import User
from app.models.register_user import RegisterUser
from app.services.user_service import UserService
from app.services.mail_service import MailService


router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post("/logout", responses={
    200: {"description": "Logout successful"},
    401: {"description": "Invalid refresh token"},
    500: {"description": "Internal server error"},
})
async def logout(refresh_token: str = Depends(AuthService.oauth2_scheme)) -> Response:
    """Logout a user."""
    user_info = AuthService.decode_token(refresh_token)
    if user_info:
        user = await User.find(User.email == user_info["sub"]).first_or_none()
        if user:
            await user.save()
    return Response(status_code=status.HTTP_200_OK)


@router.post("/login", response_model=Token, responses={
    401: {"description": "Incorrect email or password"},
    500: {"description": "Internal server error"},
})
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login for access token. """
    logger.info("Login attempt for %s", form_data.username)
    user = await AuthService.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not verified",
        )

    return AuthService.generate_app_token(user)


@router.post("/signup",  responses={
    200: {"description": "User registered successfully"},
    400: {"description": "Email already exists"},
    500: {"description": "Internal server error"},
})
async def register(user: RegisterUser, mail_service: MailService = Depends(MailService)):
    """Register a new user."""
    found_user = await User.find(User.email == user.email).first_or_none()
    if found_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    if user.token:
        try:
            user_invite, email, account_id, role = await AuthService.verify_invite_user_to_account_token(user.token)
            if not user_invite.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token",
                )

            invitation = await AccountInvitation.find(AccountInvitation.account_id == account_id, AccountInvitation.email == email).first_or_none()

            if not invitation:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid token",
                )

            new_user = User(
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                role=role,
                account_id=account_id,
                disabled=False,
                verified=False,
                hashed_password=AuthService.pwd_context.hash(user.password),
                terms_and_conditions_accepted=user.terms_and_conditions_accepted,
            )

            await UserService.create_user_from_invitation(new_user)

            verify_token = await AuthService.create_verify_register_token(new_user.id, new_user.account_id)
            mail_service.send_verify_register_email(
                new_user.email, verify_token)

            await invitation.delete()

        except HTTPException as e:
            await new_user.delete()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            ) from e

    else:
        new_user = User(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=Role.OWNER,
            disabled=False,
            verified=False,
            hashed_password=AuthService.pwd_context.hash(user.password),
            terms_and_conditions_accepted=user.terms_and_conditions_accepted,
        )

        await UserService.create_user_and_account(new_user, user.account_name)
        token = await AuthService.create_verify_register_token(new_user.id, new_user.account_id)
        mail_service.send_verify_register_email(new_user.email, token)

    return {"message": "User registered successfully"}


@router.get("/verify-register", responses={
    200: {"description": "User verified successfully"},
    400: {"description": "Invalid token"},
    500: {"description": "Internal server error"},
})
async def verify_register(token: str):
    """Verify a user's registration."""

    await AuthService.verify_register_token(token)

    return {"message": "User verified successfully"}


@router.post("/forgot-password", responses={
    200: {"description": "Password reset email sent"},
    400: {"description": "Email not found"},
    500: {"description": "Internal server error"},
})
async def forgot_password(request: ForgotPasswordRequest, mail_service: MailService = Depends(MailService)):
    """Send a password reset email."""
    user = await User.find(User.email == request.email).first_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not found",
        )
    token = await AuthService.create_forgot_password_token(user.id, user.account_id)
    mail_service.send_forgot_password_email(user.email, token)

    return {"message": "Password reset email sent"}


@router.post("/reset-password", responses={
    200: {"description": "Password reset successfully"},
    400: {"description": "Invalid token"},
    500: {"description": "Internal server error"},
})
async def reset_password(request: ResetPasswordRequest):
    """Reset a user's password."""
    user = await AuthService.verify_forgot_password_token(request.token)
    user.hashed_password = AuthService.pwd_context.hash(request.password)
    await user.save()

    return {"message": "Password reset successfully"}


@router.post("/refresh", response_model=Token, responses={
    401: {"description": "Invalid refresh token"},
    400: {"description": "Invalid user"},
    500: {"description": "Internal server error"},
})
async def refresh_access_token(refresh_token: str = Depends(AuthService.oauth2_scheme)):
    """Refresh access token."""
    user_info = AuthService.decode_token(refresh_token)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    user = await User.find(User.email == user_info["sub"]).first_or_none()
    if not user or user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user"
        )
    return AuthService.generate_app_token(user)
