

from pydantic import BaseModel
from pydantic import Field

from app.enums.role import Role


class InviteUserToAccount(BaseModel):
    """Model for inviting a user to an account."""
    email: str = Field(..., description="The email of the user to invite")
    role: Role = Field(..., description="The role of the user to invite")
