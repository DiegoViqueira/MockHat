"""Account Service"""
from datetime import datetime, UTC
import logging
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.account import Account
from app.enums.role import Role
from app.models.account_invitations import AccountInvitation, ListInvitations
from app.models.user import User
from app.enums.plan import Plan


class AccountService:
    """Service for managing account-related operations."""

    @staticmethod
    async def create_account(name: str, owner: User, plan: Plan = Plan.FREE) -> Account:
        """Creates a new account.

        Args:
            name (str): Account name
            plan (Plan, optional): Account plan. Defaults to Plan.FREE

        Returns:
            Account: The created account

        Raises:
            HTTPException: If there's an error creating the account
        """
        try:
            account = Account(
                name=name,
                plan=plan,
                users=[]
            )

            await account.create()

            # Update owner's account_id
            owner.account_id = str(account.id)
            await owner.save()
            account.users = [owner.id]
            await account.save()
            return account

        except HTTPException:
            logging.error("Error creating account: %s", e)
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            logging.error("Error creating account: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating account"
            ) from e

    @staticmethod
    async def get_account(account_id: str) -> Optional[Account]:
        """Gets an account by its ID."""
        return await Account.get(account_id)

    @staticmethod
    async def update_account(account_id: str, name: str, plan: Optional[Plan] = None) -> Account:
        """Updates account data."""
        try:
            account = await Account.get(account_id)
            if not account:
                raise HTTPException(
                    status_code=404, detail="Account not found")

            account.name = name
            if plan:
                account.plan = plan
            account.updated_at = datetime.now(UTC)

            await account.save()
            return account

        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating account"
            ) from e

    @staticmethod
    async def get_account_admins(account_id: str) -> List[User]:
        """Gets all admins of an account."""
        account = await Account.get(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")

        admins = []

        if account.users:
            for user_id in account.users:
                user = await User.get(user_id)
                if user.is_admin:
                    admins.append(user)
        return admins

    @staticmethod
    async def add_user_to_account(account_id: str, user: User) -> Account:
        """Adds a user to a Business account."""
        try:
            account = await Account.get(account_id)
            if not account:
                raise HTTPException(
                    status_code=404, detail="Account not found")

            # TODO: Remove this once we have a way to upgrade the account plan
            # if account.plan != Plan.BUSINESS:
            #     raise HTTPException(
            #         status_code=status.HTTP_400_BAD_REQUEST,
            #         detail="Only Business accounts can have multiple users"
            #     )

            if account.users is None:
                account.users = []

            account.users.append(user.id)
            await account.save()
            return account

        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding user to account"
            ) from e

    @staticmethod
    async def remove_user_from_account(account_id: str, user_id: str) -> Account:
        """Removes a user from a Business account."""
        try:
            account = await Account.get(account_id)
            if not account:
                raise HTTPException(
                    status_code=404, detail="Account not found")

            if account.users is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Account has no users"
                )

            # Remove user from list
            account.users = [u for u in account.users if u != user_id]
            await account.save()

            # Update user
            user = await User.get(user_id)
            if user:
                user.account_id = ""
                await user.save()

            return account

        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error removing user from account"
            ) from e

    @staticmethod
    async def list_invitations_by_account(account_id: str) -> ListInvitations:
        """List invitations by account."""
        try:
            invitations = await AccountInvitation.find(
                AccountInvitation.account_id == account_id).to_list()

            list_invitations = ListInvitations(
                invitations=invitations,
                total=len(invitations)
            )

            return list_invitations
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing invitations"
            ) from e
