import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException

from app.models.user import User
from app.enums.role import Role
from app.services.user_service import UserService
from app.services.account_service import AccountService


@pytest.mark.asyncio
class TestUserService:
    """Test suite for UserService."""

    async def test_get_user_by_email(self, mock_db):
        """Test getting a user by email."""
        # Arrange
        email = "user@example.com"
        user = User(email=email)
        await user.create()

        # Act
        result = await UserService.get_user_by_email(email)
        # Assert
        assert result is not None
        assert result.email == email

    async def test_create_user_and_account_success(self, mock_db):
        """Test successful user and account creation."""
        # Arrange
        test_user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=Role.MEMBER
        )
        mock_account = MagicMock(id="test_account_id")

        with patch.object(User, 'create', return_value=test_user), \
                patch.object(AccountService, 'create_account', return_value=mock_account):
            # Act
            result = await UserService.create_user_and_account(test_user)
            # Assert
            assert result.account_id == "test_account_id"

    async def test_create_user_and_account_failure(self, mock_db):
        """Test user and account creation failure."""
        # Arrange
        test_user = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=Role.MEMBER
        )

        with patch.object(User, 'create'), \
                patch.object(User, 'delete'), \
                patch.object(AccountService, 'create_account', side_effect=Exception("Test error")):

            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await UserService.create_user_and_account(test_user)

            assert exc_info.value.status_code == 500
            assert "Error creating user and account" in str(
                exc_info.value.detail)

    async def test_update_user_success(self, mock_db):
        """Test successful user update."""
        # Arrange
        user = User(
            email="old@example.com",
            first_name="Old",
            last_name="User"
        )
        await user.create()

        update_data = User(
            email="new@example.com",
            first_name="New",
            last_name="User",
            role=Role.MEMBER
        )

        # Act
        result = await UserService.update_user(str(user.id), update_data)

        # Assert
        assert result.email == update_data.email
        assert result.first_name == update_data.first_name

        # Verify in database
        updated_user = await User.get(user.id)
        assert updated_user.email == update_data.email

    async def test_update_user_not_found(self, mock_db):
        """Test user update when user not found."""
        # Arrange
        user_id = "nonexistent_id"
        user_data = User(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role=Role.MEMBER
        )

        with patch.object(User, 'get', return_value=None):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await UserService.update_user(user_id, user_data)
            assert exc_info.value.status_code == 404

    async def test_delete_user_success(self, mock_db):
        """Test successful user deletion."""
        # Arrange
        user_id = "test_id"
        mock_user = User(email="test@example.com")

        with patch.object(User, 'get', return_value=mock_user), \
                patch.object(User, 'delete'):

            # Act
            result = await UserService.delete_user(user_id)

            # Assert
            assert result is True

    async def test_delete_user_not_found(self, mock_db):
        """Test user deletion when user not found."""
        # Arrange
        user_id = "nonexistent_id"
        with patch.object(User, 'get', return_value=None):
            # Act & Assert
            with pytest.raises(HTTPException) as exc_info:
                await UserService.delete_user(user_id)
            assert exc_info.value.status_code == 404
