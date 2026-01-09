import pytest
from fastapi import HTTPException

from app.models.account import Account
from app.models.user import User
from app.enums.plan import Plan
from app.services.account_service import AccountService


@pytest.mark.asyncio
class TestAccountService:
    """Test suite for AccountService."""

    async def test_create_account_success(self, mock_db):
        """Test successful account creation."""
        # Arrange
        name = "Test Account"
        owner = User(
            email="test@example.com",
            first_name="Test",
            last_name="User"
        )
        await owner.create()

        # Act
        result = await AccountService.create_account(name, owner)

        # Assert
        assert result is not None
        assert result.name == name
        assert result.owner == owner.id

        # Verify in database
        saved_account = await Account.get(result.id)
        assert saved_account is not None
        assert saved_account.name == name
        assert saved_account.owner == owner.id

    async def test_create_account_with_business_plan(self, mock_db):
        """Test creating a business account."""
        # Arrange
        name = "Business Account"
        owner = User(
            email="business@example.com",
            first_name="Business",
            last_name="Owner"
        )
        await owner.create()

        # Act
        result = await AccountService.create_account(name, owner, Plan.BUSINESS)

        # Assert
        assert result.plan == Plan.BUSINESS
        assert isinstance(result.users, list)
        assert len(result.users) == 0

    async def test_update_account_success(self, mock_db):
        """Test successful account update."""
        # Arrange
        owner = User(email="owner@example.com")
        await owner.create()

        account = Account(
            name="Old Name",
            plan=Plan.FREE,
            owner=owner.id
        )
        await account.create()

        new_name = "Updated Account"
        new_plan = Plan.BUSINESS

        # Act
        result = await AccountService.update_account(str(account.id), new_name, new_plan)

        # Assert
        assert result.name == new_name
        assert result.plan == new_plan

        # Verify in database
        updated_account = await Account.get(account.id)
        assert updated_account.name == new_name
        assert updated_account.plan == new_plan

    async def test_add_user_to_account_success(self, mock_db):
        """Test successfully adding user to business account."""
        # Arrange
        owner = User(email="owner@example.com")
        await owner.create()

        user = User(email="user@example.com")
        await user.create()

        account = Account(
            name="Test Account",
            plan=Plan.BUSINESS,
            owner=owner.id,
            users=[]
        )
        await account.create()

        # Act
        result = await AccountService.add_user_to_account(str(account.id), user)

        # Assert
        assert user.id in result.users

        # Verify in database
        updated_account = await Account.get(account.id)
        assert user.id in updated_account.users
        updated_user = await User.get(user.id)
        assert updated_user.account_id == str(account.id)

    async def test_add_user_to_non_business_account_fails(self, mock_db):
        """Test adding user to non-business account fails."""
        # Arrange
        owner = User(email="owner@example.com")
        await owner.create()

        user = User(email="user@example.com")
        await user.create()

        account = Account(
            name="Free Account",
            plan=Plan.FREE,
            owner=owner.id
        )
        await account.create()

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await AccountService.add_user_to_account(str(account.id), user)

        assert exc_info.value.status_code == 400
        assert "Only Business accounts can have multiple users" in str(
            exc_info.value.detail)

    async def test_remove_user_from_account_success(self, mock_db):
        """Test successfully removing user from account."""
        # Arrange
        owner = User(email="owner@example.com")
        await owner.create()

        user = User(email="user@example.com")
        await user.create()

        account = Account(
            name="Test Account",
            plan=Plan.BUSINESS,
            owner=owner.id,
            users=[user.id]
        )
        await account.create()

        user.account_id = str(account.id)
        await user.save()

        # Act
        result = await AccountService.remove_user_from_account(account.id, user.id)

        # Assert
        assert user.id not in result.users

        # Verify in database
        updated_account = await Account.get(account.id)
        assert user.id not in updated_account.users
        updated_user = await User.get(user.id)
        assert updated_user.account_id == ""

    async def test_remove_user_from_account_not_found(self, mock_db):
        """Test removing user from non-existent account."""
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await AccountService.remove_user_from_account("nonexistent_id", "user_id")

        assert exc_info.value.status_code == 404
        assert "Account not found" in str(exc_info.value.detail)
