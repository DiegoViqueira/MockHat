"""Role"""
from enum import Enum


class Role(Enum):
    """Enum for user roles"""
    ADMIN = 'Administrator'
    MEMBER = 'Member'
    OWNER = 'Owner'
