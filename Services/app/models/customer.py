"""Model Customer"""
from pydantic import BaseModel, Field


class CustomerPortalResponse(BaseModel):
    """
    Response model for customer portal
    """
    portal_url: str = Field('')


class CustomerPortalRequest(BaseModel):
    """
    Request model for customer portal
    """
    fallback_url: str = Field(default='')
