"""Model User"""
from datetime import datetime, UTC
from typing import Optional, List
from beanie import Document, Update, Save, before_event
from pymongo import IndexModel
from pydantic import Field, BaseModel
import ulid
from app.enums.role import Role


class User(Document):
    """User model"""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    account_id: str = Field(default='', description="Account ID")
    email: str = Field(..., description="Email")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    role: Role = Field(default=Role.MEMBER, description="Role")
    disabled: bool = Field(default=False, description="Disabled")
    verified: bool = Field(default=False, description="Verified")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Created at")
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Updated at")
    hashed_password: Optional[str] = Field(
        default='', description="Hashed password", exclude=True)

    terms_and_conditions_accepted: Optional[bool] = Field(
        default=False, description="Terms and conditions accepted")

    @before_event(Save, Update)
    async def set_updated_at(self):
        """Set the updated_at field to the current UTC time"""
        self.updated_at = datetime.now(UTC)

    class Settings:
        """Settings for the User model"""
        name = "users"
        indexes = [
            IndexModel(
                [("email", 1)],
                unique=True
            ),
            [
                ("account_id", 1),
            ]
        ]

    @property
    def is_admin(self):
        """Check if the user is an admin"""
        return self.role == Role.ADMIN or self.role == Role.OWNER

    @property
    def is_owner(self):
        """Check if the user is an owner"""
        return self.role == Role.OWNER

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, User):
            return self.id == other.id
        return False


class ListUsers(BaseModel):
    """List of users"""
    users: List[User]
    total: int
