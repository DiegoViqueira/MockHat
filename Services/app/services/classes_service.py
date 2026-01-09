"""Classes Service"""
import logging
from typing import Optional, List
from fastapi import HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.models.classes import Class, ListClass
from app.models.writing import Writing
from app.models.user import User
from app.services.user_service import UserService


class ClassesService:
    """Servicio para gestionar operaciones relacionadas con clases."""

    @staticmethod
    async def get_class_ai_messages(class_id: str) -> List[str]:
        """Obtiene los mensajes de una clase."""
        writings = await Writing.find(Writing.class_id == class_id).to_list()
        return [writing.ai_feedback.model_dump_json() for writing in writings]

    @staticmethod
    async def create_class(class_: Class, user: User) -> Class:
        """Crea una nueva clase."""
        try:
            if not user.is_admin:
                raise HTTPException(
                    status_code=403,
                    detail="You are not allowed to create a class"
                )

            class_.account_id = user.account_id
            await class_.create()

            # Añadir administradores a la lista de profesores de cada clase
            service = UserService()
            admin_users = await service.list_admin_users_by_account(user.account_id)

            class_.teachers.extend(admin_users.users)
            return class_

        except DuplicateKeyError as e:
            raise HTTPException(
                status_code=400,
                detail="Class already exists"
            ) from e
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating class"
            ) from e

    @staticmethod
    async def get_class(class_id: str, user: User) -> Class:
        """Obtiene una clase por su ID."""
        try:
            if user.is_admin:
                class_ = await Class.find_one(
                    Class.account_id == user.account_id,
                    Class.id == class_id
                )
            else:
                class_ = await Class.find_one(
                    Class.teachers == {"$elemMatch": {"_id": user.id}},
                    Class.account_id == user.account_id,
                    Class.id == class_id
                )

            if not class_:
                raise HTTPException(
                    status_code=404,
                    detail="Class not found"
                )

            # Añadir administradores a la lista de profesores
            service = UserService()
            admin_users = await service.list_admin_users_by_account(user.account_id)
            class_.teachers.extend(admin_users.users)

            return class_

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error getting class"
            ) from e

    @staticmethod
    async def list_classes(
        user: User,
        limit: int = 10,
        skip: int = 0,
        is_active: Optional[bool] = None,
        search: Optional[str] = None
    ) -> ListClass:
        """Lista todas las clases del profesor o admin con paginación."""
        try:
            query = {}

            if search:
                search_query = {"$regex": search, "$options": "i"}
                query["$or"] = [
                    {"name": search_query},
                    {"description": search_query}
                ]

            if is_active is not None:
                query["is_active"] = is_active

            query["account_id"] = user.account_id

            if not user.is_admin:
                query["teachers"] = {"$elemMatch": {"_id": user.id}}

            classes = await Class.find(query).sort("name").skip(skip).limit(limit).to_list()

            total = await Class.find(query).count()

            # Añadir administradores a la lista de profesores de cada clase
            service = UserService()
            admin_users = await service.list_admin_users_by_account(user.account_id)

            for class_ in classes:
                class_.teachers.extend(admin_users.users)

            return ListClass(
                classes=classes,
                total=total
            )

        except Exception as e:
            logging.error("Error listing classes: %s", e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error listing classes"
            ) from e

    @staticmethod
    async def update_class(class_id: str, class_update: Class, user: User) -> Class:
        """Actualiza una clase existente."""
        try:
            if not user.is_admin:
                raise HTTPException(
                    status_code=403,
                    detail="You are not allowed to update this class"
                )

            class_ = await Class.find_one(
                Class.id == class_id,
                Class.account_id == user.account_id
            )

            if not class_:
                raise HTTPException(
                    status_code=404,
                    detail="Class not found"
                )

            # Eliminar duplicados
            class_update.teachers = list(set(class_update.teachers))

            # Eliminar administradores de la lista de profesores
            class_update.teachers = [
                teacher for teacher in class_update.teachers if not teacher.is_admin]

            class_update.students = list(set(class_update.students))

            # Actualizar campos
            class_.teachers = class_update.teachers if class_update.teachers else []
            class_.name = class_update.name
            class_.description = class_update.description
            class_.students = class_update.students if class_update.students else []
            class_.is_active = class_update.is_active

            await class_.save()

            # Añadir administradores a la lista de profesores de cada clase
            service = UserService()
            admin_users = await service.list_admin_users_by_account(user.account_id)

            class_.teachers.extend(admin_users.users)

            return class_

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error updating class"
            ) from e
