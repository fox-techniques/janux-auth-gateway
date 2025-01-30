"""
test_mongoDB.py

Unit tests for MongoDB initialization, super admin creation, and authentication.

Tests:
- Database initialization
- Ensure super admin exists
- User authentication with correct and incorrect credentials
- Admin authentication with correct and incorrect credentials
- Username lookup

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from unittest.mock import patch
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from janux_auth_gateway.database.mongoDB import (
    init_db,
    ensure_super_admin_exists,
    authenticate_user,
    authenticate_admin,
    username_exists,
)
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.admin import Admin
from janux_auth_gateway.auth.passwords import hash_password
from janux_auth_gateway.config import Config


@pytest.fixture(scope="function")
async def mock_db(mocker):
    """
    Provides a fully isolated MongoDB for testing.
    Ensures Beanie is initialized properly.
    Cleans up test data after each test.
    """
    db_name = f"test_db_{uuid.uuid4().hex}"  # Unique test database for each run
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Local MongoDB
    test_db = client[db_name]

    # Initialize Beanie models for test database
    await init_beanie(database=test_db, document_models=[User, Admin])

    # Patch the MongoDB client so `init_db()` uses the mock DB
    mocker.patch(
        "janux_auth_gateway.database.mongoDB.AsyncIOMotorClient", return_value=client
    )

    yield test_db  # Provide test DB to tests

    # Cleanup: Drop test database after each test
    await client.drop_database(db_name)


@pytest.mark.asyncio
async def test_init_db_success(mock_db):
    """
    Test successful MongoDB initialization.

    Expected Outcome:
    - Connection succeeds without raising an error.
    """
    try:
        await init_db()
    except SystemExit:
        pytest.fail("init_db() raised SystemExit unexpectedly!")


@pytest.mark.asyncio
async def test_ensure_super_admin_exists(mock_db, mocker):
    """
    Test that `ensure_super_admin_exists()` creates an admin if none exists.

    Expected Outcome:
    - If no admin exists, a new one is created.
    """
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    assert await Admin.find_one(Admin.email == "admin@example.com") is None

    await ensure_super_admin_exists()

    admin = await Admin.find_one(Admin.email == "admin@example.com")
    assert admin is not None
    assert admin.email == "admin@example.com"
    assert admin.role == "super_admin"


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_db):
    """
    Test user authentication with correct credentials.

    Expected Outcome:
    - The function should return True for valid credentials.
    """
    user = User(
        email="user@example.com",
        full_name="Test User",
        hashed_password=hash_password("securepassword"),
    )
    await user.save()

    assert await authenticate_user("user@example.com", "securepassword") is True


@pytest.mark.asyncio
async def test_authenticate_user_fail(mock_db):
    """
    Test user authentication failure due to incorrect password.

    Expected Outcome:
    - The function should return False when the password is incorrect.
    """
    user = User(
        email="user@example.com",
        full_name="Test User",
        hashed_password=hash_password("securepassword"),
    )
    await user.save()

    assert await authenticate_user("user@example.com", "wrongpassword") is False


@pytest.mark.asyncio
async def test_authenticate_admin_success(mock_db, mocker):
    """
    Test admin authentication with correct credentials.

    Expected Outcome:
    - The function should return True for valid credentials.
    """
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    admin = Admin(
        email="admin@example.com",
        full_name="Super Admin",
        hashed_password=hash_password("adminpassword"),
    )
    await admin.save()

    assert await authenticate_admin("admin@example.com", "adminpassword") is True


@pytest.mark.asyncio
async def test_authenticate_admin_fail(mock_db, mocker):
    """
    Test admin authentication failure due to incorrect password.

    Expected Outcome:
    - The function should return False when the password is incorrect.
    """
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    admin = Admin(
        email="admin@example.com",
        full_name="Super Admin",
        hashed_password=hash_password("adminpassword"),
    )
    await admin.save()

    assert await authenticate_admin("admin@example.com", "wrongpassword") is False


@pytest.mark.asyncio
async def test_username_exists_found(mock_db):
    """
    Test `username_exists()` when the user exists.

    Expected Outcome:
    - The function should return the user object when the username exists.
    """
    user = User(
        email="existing@example.com",
        full_name="Existing User",
        hashed_password=hash_password("securepassword"),
    )
    await user.save()

    found_user = await username_exists("existing@example.com")
    assert found_user is not None
    assert found_user.email == "existing@example.com"


@pytest.mark.asyncio
async def test_username_exists_not_found(mock_db):
    """
    Test `username_exists()` when the user does not exist.

    Expected Outcome:
    - The function should return None when the username is not found.
    """
    found_user = await username_exists("nonexistent@example.com")
    assert found_user is None
