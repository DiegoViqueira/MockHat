"""Accounts"""
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.requests import Request

from app.models.account import AccountDto
from app.models.account_invitations import AccountInvitation, ListInvitations
from app.models.invite_user_to_account import InviteUserToAccount
from app.services.account_service import AccountService
from app.services.mail_service import MailService
from app.services.user_service import UserService
from app.services.auth_service import AuthService
router = APIRouter(prefix='/accounts', tags=["Accounts"])


@router.post("/invite-user", status_code=status.HTTP_200_OK,
             responses={
                 404: {"description": "Account not found"},
                 500: {"description": "Internal server error"},
             })
async def invite_user(
        request: Request,
        invited_user: InviteUserToAccount,
        auth_service: AuthService = Depends(AuthService),
        mail_service: MailService = Depends(MailService)):
    """Invite a user to an account."""

    user = request.state.user

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    user_exists = await UserService.get_user_by_email(invited_user.email)

    if user_exists:
        raise HTTPException(status_code=400, detail="User already exists")

    account = await AccountService.get_account(user.account_id)

    token = await auth_service.create_invite_user_to_account_token(
        user.id, invited_user.email, account.name, account.id, invited_user.role)

    invitation = AccountInvitation(
        account_id=account.id, email=invited_user.email, role=invited_user.role, token=token)

    await invitation.save()

    mail_service.send_invite_user_to_account_email(
        invited_user.email, token, account.name)

    return {"message": "User invited successfully"}


@router.get("", response_model=AccountDto, status_code=status.HTTP_200_OK,
            responses={
                404: {"description": "Account not found"},
                500: {"description": "Internal server error"},
            })
async def get_account(
        request: Request,
        service: AccountService = Depends(AccountService)):
    """Get an account by its ID extracted from the token."""
    try:
        user = request.state.user
        account = await service.get_account(user.account_id)
        users = []

        if account.users:
            users = [await UserService.get_user(user_id) for user_id in account.users]

        account_dto = AccountDto(
            id=account.id,
            name=account.name,
            plan=account.plan,
            users=users,
            created_at=account.created_at,
            updated_at=account.updated_at,
            is_active=account.is_active
        )
        return account_dto

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error("Error getting account: %s", e)
        raise HTTPException(
            status_code=500, detail="Internal server error") from e


@router.get("/invitations", response_model=ListInvitations,
            responses={
                500: {"description": "Internal server error"},
                403: {"description": "User is not an admin"},
                404: {"description": "User does not exist"},
            })
async def list_invitations(request: Request, service: AccountService = Depends(AccountService)):
    """Get a list of invitations."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not an admin")

    invitations = await service.list_invitations_by_account(user.account_id)
    return invitations
