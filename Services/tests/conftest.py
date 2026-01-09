"""Conftest"""
import pytest_asyncio
import motor.motor_asyncio
from beanie import init_beanie

from app.models.user import User
from app.core.settings import settings
from app.models.account import Account


@pytest_asyncio.fixture
async def mock_db():
    """Create a real test database connection."""
    client = motor.motor_asyncio.AsyncIOMotorClient(
        settings.mongo.MONGO_TEST_URI)
    db = client.get_database(settings.mongo.MONGO_TEST_DATABASE)

    await init_beanie(
        database=db,
        document_models=[User, Account]
    )

    yield db  # Yield allows cleanup after test execution

    for collection in await db.list_collection_names():
        await db.drop_collection(collection)

    client.close()
