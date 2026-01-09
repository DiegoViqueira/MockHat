"""Users"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from starlette.requests import Request


from app.core.settings import settings
from app.services.auth_service import AuthService
from app.models.user import User, ListUsers
from app.services.user_service import UserService

router = APIRouter(prefix='/users', tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED,
             responses={
                 400: {"description": "User already exists"},
                 500: {"description": "Internal server error"},
             })
async def create_user(
        request: Request,
        user: User,
        service: UserService = Depends(UserService)
):
    """Create a new user."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not an admin")

    new_user = await service.find(email=user.email)

    if len(new_user) == 0:
        hashed_password = AuthService.pwd_context.hash(
            settings.auth.ADMIN_PASSWORD)
        new_user = User(**user.dict())
        new_user.hashed_password = hashed_password
        await service.create(new_user)

        return Response(status_code=status.HTTP_201_CREATED)

    raise HTTPException(status_code=400, detail="User already exists")


@router.get("/{user_id}", response_model=User,
            responses={
                404: {"description": "User not found"},
                500: {"description": "Internal server error"},
                403: {"description": "User is not an admin"},
            })
async def get_user(
        request: Request,
        user_id: str, service: UserService = Depends(UserService),
):
    """Get a user by their ID."""

    user = request.state.user
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not an admin")

    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    return user


@router.get("/active/all", response_model=ListUsers,
            responses={
                404: {"description": "User not found"},
                500: {"description": "Internal server error"},
            })
async def get_actives_users_by_account(request: Request,
                                       service: UserService = Depends(UserService)):
    """Get a list of active users by account."""
    logging.info("get_actives_users_by_account")
    user = request.state.user
    logging.info(user)
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        return ListUsers(users=[], total=0)

    users = await service.list_users_by_account(user.account_id)

    return users


@router.get("/active/me", response_model=User,
            responses={
                404: {"description": "User not found"},
                500: {"description": "Internal server error"},
            })
async def read_users_me(request: Request):
    """Get the currently authenticated user."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    return user


@router.patch("/{user_id}", response_model=User,
              responses={
                  403: {"description": "User is not an admin"},
                  404: {"description": "User not found"},
                  500: {"description": "Internal server error"},
              })
async def update_user(
        request: Request,
        user_id: str,
        user: User,
        service: UserService = Depends(UserService)
) -> Response:
    """Update a user's information."""

    user = request.state.user

    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        raise HTTPException(status_code=403, detail="User is not an admin")

    updated_user = await service.get_user(user_id)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User does not exist")

    updated_user.email = user.email
    updated_user.avatar = user.avatar
    updated_user.gender = user.gender
    updated_user.first_name = user.first_name
    updated_user.last_name = user.last_name
    updated_user.level = user.level
    updated_user.disabled = user.disabled
    updated_user.role = user.role
    await updated_user.save()


@router.get("", response_model=ListUsers,
            responses={
                500: {"description": "Internal server error"},
                403: {"description": "User is not an admin"},
                404: {"description": "User does not exist"},
            })
async def list_users(request: Request, limit: int = Query(10, alias="limit"), skip: int = Query(0, alias="offset"),
                     service: UserService = Depends(UserService)):
    """Get a paginated list of users."""
    user = request.state.user
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")

    if not user.is_admin:
        return ListUsers(users=[], total=0)

    users = await service.list_users_by_account(user.account_id, skip, limit)
    return users
