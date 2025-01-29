"""
test_mongoDB.py

Unit tests for the MongoDB database connection and authentication module in the JANUX Authentication Gateway.

Tests:
- Database connection initialization.
- Super admin account creation.
- User and admin authentication.
- User and admin existence checks.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import AsyncMock, patch
from janux_auth_gateway.database.mongoDB import (
    init_db,
    ensure_super_admin_exists,
    authenticate_user,
    authenticate_admin,
    username_exists,
    admin_username_exists,
)
from janux_auth_gateway.config import Config
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.admin import Admin


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.AsyncIOMotorClient")
async def test_init_db_success(mock_client):
    """
    Test successful MongoDB initialization.

    Steps:
    1. Mock MongoDB client connection.
    2. Call `init_db()`.

    Expected Outcome:
    - No exceptions should be raised.
    """
    mock_client.return_value.server_info = AsyncMock(return_value=True)

    try:
        await init_db()
    except SystemExit:
        pytest.fail("init_db() raised SystemExit unexpectedly.")


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.AsyncIOMotorClient")
async def test_init_db_failure(mock_client):
    """
    Test MongoDB initialization failure.

    Steps:
    1. Mock MongoDB client to raise an error.
    2. Call `init_db()`.

    Expected Outcome:
    - The function should raise `SystemExit`.
    """
    mock_client.return_value.server_info.side_effect = Exception("Connection failed")

    with pytest.raises(SystemExit):
        await init_db()


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.Admin.find_one", new_callable=AsyncMock)
@patch("janux_auth_gateway.database.mongoDB.Admin.insert", new_callable=AsyncMock)
async def test_ensure_super_admin_exists(admin_insert_mock, find_admin_mock):
    """
    Test super admin creation when missing.

    Steps:
    1. Mock `Admin.find_one()` to return `None` (admin does not exist).
    2. Call `ensure_super_admin_exists()`.
    3. Verify `Admin.insert()` is called.

    Expected Outcome:
    - The function should create a new super admin.
    """
    find_admin_mock.return_value = None

    await ensure_super_admin_exists()
    admin_insert_mock.assert_called_once()


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.Admin.find_one", new_callable=AsyncMock)
async def test_ensure_super_admin_exists_already_exists(find_admin_mock):
    """
    Test that no new super admin is created if one already exists.

    Steps:
    1. Mock `Admin.find_one()` to return an existing admin.
    2. Call `ensure_super_admin_exists()`.
    3. Verify `Admin.insert()` is NOT called.

    Expected Outcome:
    - No new super admin should be created.
    """
    find_admin_mock.return_value = Admin(email="admin@example.com", role="super_admin")

    await ensure_super_admin_exists()
    find_admin_mock.assert_called_once()


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.username_exists", new_callable=AsyncMock)
@patch("janux_auth_gateway.auth.passwords.verify_password", return_value=True)
async def test_authenticate_user_success(mock_verify_password, mock_username_exists):
    """
    Test user authentication with correct credentials.

    Steps:
    1. Mock `username_exists()` to return a user object.
    2. Mock `verify_password()` to return `True`.
    3. Call `authenticate_user()` with correct credentials.

    Expected Outcome:
    - The function should return `True`.
    """
    mock_username_exists.return_value = User(
        email="testuser@example.com", hashed_password="hashedpassword"
    )

    result = await authenticate_user("testuser@example.com", "correctpassword")
    assert result is True


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.username_exists", new_callable=AsyncMock)
@patch("janux_auth_gateway.auth.passwords.verify_password", return_value=False)
async def test_authenticate_user_invalid_password(
    mock_verify_password, mock_username_exists
):
    """
    Test user authentication failure due to incorrect password.

    Steps:
    1. Mock `username_exists()` to return a user object.
    2. Mock `verify_password()` to return `False`.
    3. Call `authenticate_user()` with incorrect credentials.

    Expected Outcome:
    - The function should return `False`.
    """
    mock_username_exists.return_value = User(
        email="testuser@example.com", hashed_password="hashedpassword"
    )

    result = await authenticate_user("testuser@example.com", "wrongpassword")
    assert result is False


@pytest.mark.asyncio
@patch(
    "janux_auth_gateway.database.mongoDB.admin_username_exists", new_callable=AsyncMock
)
@patch("janux_auth_gateway.auth.passwords.verify_password", return_value=True)
async def test_authenticate_admin_success(mock_verify_password, mock_admin_exists):
    """
    Test admin authentication with correct credentials.

    Steps:
    1. Mock `admin_username_exists()` to return an admin object.
    2. Mock `verify_password()` to return `True`.
    3. Call `authenticate_admin()` with correct credentials.

    Expected Outcome:
    - The function should return `True`.
    """
    mock_admin_exists.return_value = Admin(
        email="admin@example.com", hashed_password="hashedpassword"
    )

    result = await authenticate_admin("admin@example.com", "correctpassword")
    assert result is True


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.User.find_one", new_callable=AsyncMock)
async def test_username_exists(mock_find_one):
    """
    Test checking if a username exists in the database.

    Steps:
    1. Mock `User.find_one()` to return a user object.
    2. Call `username_exists()`.

    Expected Outcome:
    - The function should return the user object.
    """
    mock_find_one.return_value = User(email="test@example.com")

    result = await username_exists("test@example.com")
    assert result is not None
    assert result.email == "test@example.com"


@pytest.mark.asyncio
@patch("janux_auth_gateway.database.mongoDB.Admin.find_one", new_callable=AsyncMock)
async def test_admin_username_exists(mock_find_one):
    """
    Test checking if an admin username exists in the database.

    Steps:
    1. Mock `Admin.find_one()` to return an admin object.
    2. Call `admin_username_exists()`.

    Expected Outcome:
    - The function should return the admin object.
    """
    mock_find_one.return_value = Admin(email="admin@example.com")

    result = await admin_username_exists("admin@example.com")
    assert result is not None
    assert result.email == "admin@example.com"
