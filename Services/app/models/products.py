"""Model Products"""
from datetime import datetime, UTC
from typing import Dict
from pymongo import IndexModel
from beanie import Document
from pydantic import Field
import ulid


class Products(Document):
    """Model for storing product information."""
    id: str = Field(default_factory=lambda: str(ulid.ULID()))
    name: str = Field('')
    stripe_id: str = Field('', description="stripe_id for product")
    metadata: Dict[str, str] = Field(default_factory={})
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def get_feature_by_metadata(self, key: str) -> int:
        """Get a feature by its metadata key."""
        for feat in self.features:
            if feat.metadata.get(key):
                return int(feat.metadata.get(key))

    class Settings:
        """Settings for the products collection."""
        name = "products"
        indexes = [
            IndexModel(
                [("stripe_id", 1),
                 ],
                unique=True
            )
        ]
