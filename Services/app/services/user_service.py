"""User Service"""
from datetime import datetime
import logging
from typing import Optional, List

from fastapi import HTTPException, status
from app.models.user import ListUsers, User
from app.enums.role import Role
from app.services.account_service import AccountService


class UserService:
    """Servicio para gestionar operaciones relacionadas con usuarios."""

    @staticmethod
    async def create_user(user_data: User, hashed_password: Optional[str] = None) -> User:
        """Crea un nuevo usuario."""
        try:
            new_user = User(
                email=user_data.email,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                role=user_data.role,
                disabled=user_data.disabled,
                verified=user_data.verified,
                hashed_password=hashed_password
            )
            await new_user.create()
            return new_user

        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            ) from e

    @staticmethod
    async def get_user(user_id: str) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return await User.get(user_id)

    @staticmethod
    async def get_user_by_email(email: str) -> Optional[User]:
        """Obtiene un usuario por su email."""
        return await User.find_one(User.email == email)

    @staticmethod
    async def update_user(user_id: str, user_data: User) -> Optional[User]:
        """Actualiza los datos de un usuario."""
        try:
            user = await User.get(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Actualizar campos
            user.email = user_data.email
            user.first_name = user_data.first_name
            user.last_name = user_data.last_name
            user.role = user_data.role
            user.disabled = user_data.disabled
            user.verified = user_data.verified
            await user.save()
            return user
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating user"
            ) from e

    @staticmethod
    async def delete_user(user_id: str) -> bool:
        """Elimina un usuario."""
        try:
            user = await User.get(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            await user.delete()
            return True
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting user"
            ) from e

    @staticmethod
    async def list_admin_users_by_account(account_id: str) -> ListUsers:
        """Lista usuarios con paginación y filtro opcional por rol."""
        try:
            query = {}
            query["account_id"] = account_id
            query["role"] = {"$in": [Role.ADMIN, Role.OWNER]}

            users = await User.find(query).to_list()
            total = await User.find(query).count()

            return ListUsers(users=users, total=total)
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing users"
            ) from e

    @staticmethod
    async def list_users_by_account(account_id: str, skip: int = None, limit: int = None, role: Optional[Role] = None) -> ListUsers:
        """Lista usuarios con paginación y filtro opcional por rol."""
        try:
            query = {}
            if role:
                query["role"] = role
            if account_id:
                query["account_id"] = account_id

            cursor = User.find(query)

            # Apply skip if it's not None and is an integer
            if isinstance(skip, int):
                cursor = cursor.skip(skip)

            # Apply limit if it's not None and is an integer
            if isinstance(limit, int):
                cursor = cursor.limit(limit)

            users = await cursor.to_list(None)
            total = await User.find(query).count()

            return ListUsers(users=users, total=total)
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing users"
            ) from e

    @staticmethod
    async def change_password(user_id: str, hashed_password: str) -> bool:
        """Cambia la contraseña de un usuario."""
        try:
            user = await User.get(user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Actualizar contraseña
            user.hashed_password = hashed_password
            user.updated_at = datetime.utcnow()
            await user.save()

            return True

        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error changing password"
            ) from e

    @staticmethod
    async def get_users_by_account(account_id: str, skip: int = 0, limit: int = 10) -> List[User]:
        """Obtiene usuarios por ID de cuenta."""
        try:
            users = await User.find(
                User.account_id == account_id
            ).skip(skip).limit(limit).to_list()
            return users
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting users by account"
            ) from e

    @staticmethod
    async def create_user_and_account(user: User, account_name: str):
        """Crea un usuario y una cuenta."""
        try:
            await user.create()
            account = await AccountService.create_account(account_name, user)
            user.account_id = str(account.id)
            await user.save()
            return user
        except HTTPException as e:
            logging.error("Error creating user and account: %s", e)
            await user.delete()
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            await user.delete()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user and account"
            ) from e

    @staticmethod
    async def create_user_from_invitation(user: User):
        """Crea un usuario desde una invitación."""
        try:

            await user.create()
            await AccountService.add_user_to_account(user.account_id, user)
            return user
        except HTTPException:
            raise  # ✅ Allow FastAPI HTTPException to propagate without converting it to 500

        except Exception as e:
            await user.delete()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user from invitation"
            ) from e
