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
    admin_username_exists,
)
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.admin import Admin
from janux_auth_gateway.auth.passwords import hash_password
from janux_auth_gateway.config import Config


@pytest.fixture(scope="function")
async def mock_db(mocker):
    """
    Provides a fully in-memory MongoDB for testing.
    Ensures Beanie is initialized.
    """
    db_name = f"test_db"
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # In-memory MongoDB
    test_db = client[db_name]

    # Ensure Beanie models are reinitialized
    await init_beanie(database=test_db, document_models=[User, Admin])

    # Patch the MongoDB client so `init_db()` uses the mock DB
    mocker.patch(
        "janux_auth_gateway.database.mongoDB.AsyncIOMotorClient", return_value=client
    )

    return test_db


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
    # Mock Config values to ensure function has proper credentials
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    # Ensure no admin exists before the test
    assert await Admin.find_one(Admin.email == "admin@example.com") is None

    # Run function to create the super admin
    await ensure_super_admin_exists()

    # Fetch the created admin (force reload)
    admin = await Admin.find_one(Admin.email == "admin@example.com")

    assert admin is not None  # Now an admin should exist
    assert admin.email == "admin@example.com"
    assert admin.role == "super_admin"  # Ensure correct role assignment


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_db, mocker):
    """
    Test user authentication with correct credentials.

    Expected Outcome:
    - The function should return True for valid credentials.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Insert a test user with all required fields
    user = User(
        email="user@example.com",
        full_name="Test User",  # Providing required full_name field
        hashed_password=hash_password(
            "securepassword"
        ),  # Ensure password is hashed before insert
    )
    await user.save()

    # Verify that the user now exists in the database
    inserted_user = await User.find_one(User.email == "user@example.com")
    assert inserted_user is not None, "User was not inserted into the database"

    # Run authentication function
    assert await authenticate_user("user@example.com", "securepassword") is True


@pytest.mark.asyncio
async def test_authenticate_user_fail(mock_db, mocker):
    """
    Test user authentication failure due to incorrect password.

    Expected Outcome:
    - The function should return False when the password is incorrect.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Insert a test user with all required fields
    user = User(
        email="user@example.com",
        full_name="Test User",  # Providing required full_name field
        hashed_password=hash_password(
            "securepassword"
        ),  # Ensure password is hashed before insert
    )
    await user.save()

    # Verify that the user now exists in the database
    inserted_user = await User.find_one(User.email == "user@example.com")
    assert inserted_user is not None, "User was not inserted into the database"

    # Run authentication function with an incorrect password
    assert await authenticate_user("user@example.com", "wrongpassword") is False


@pytest.mark.asyncio
async def test_authenticate_admin_success(mock_db, mocker):
    """
    Test admin authentication with correct credentials.

    Expected Outcome:
    - The function should return True for valid credentials.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Mock Config values to ensure function has proper credentials
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    # Insert a test admin with all required fields
    admin = Admin(
        email="admin@example.com",
        full_name="Super Admin",  # Providing required full_name field
        hashed_password=hash_password(
            "adminpassword"
        ),  # Ensure password is hashed before insert
    )
    await admin.save()

    # Verify that the admin now exists in the database
    inserted_admin = await Admin.find_one(Admin.email == "admin@example.com")
    assert inserted_admin is not None, "Admin was not inserted into the database"

    # Run authentication function with the correct password
    assert await authenticate_admin("admin@example.com", "adminpassword") is True


@pytest.mark.asyncio
async def test_authenticate_admin_fail(mock_db, mocker):
    """
    Test admin authentication failure due to incorrect password.

    Expected Outcome:
    - The function should return False when the password is incorrect.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Mock Config values to ensure function has proper credentials
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_EMAIL", "admin@example.com")
    mocker.patch.object(Config, "MONGO_SUPER_ADMIN_PASSWORD", "adminpassword")

    # Insert a test admin with all required fields
    admin = Admin(
        email="admin@example.com",
        full_name="Super Admin",  # Providing required full_name field
        hashed_password=hash_password(
            "adminpassword"
        ),  # Ensure password is hashed before insert
    )
    await admin.save()

    # Verify that the admin now exists in the database
    inserted_admin = await Admin.find_one(Admin.email == "admin@example.com")
    assert inserted_admin is not None, "Admin was not inserted into the database"

    # Run authentication function with an incorrect password
    assert await authenticate_admin("admin@example.com", "wrongpassword") is False


@pytest.mark.asyncio
async def test_username_exists_found(mock_db, mocker):
    """
    Test `username_exists()` when the user exists.

    Expected Outcome:
    - The function should return the user object when the username exists.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Insert a test user with all required fields
    user = User(
        email="existing@example.com",
        full_name="Existing User",  # Providing required full_name field
        hashed_password=hash_password(
            "securepassword"
        ),  # Ensure password is hashed before insert
    )
    await user.save()

    # Verify that the user now exists in the database
    inserted_user = await User.find_one(User.email == "existing@example.com")
    assert inserted_user is not None, "User was not inserted into the database"

    # Run `username_exists()` and verify the user is found
    found_user = await username_exists("existing@example.com")
    assert (
        found_user is not None
    ), "username_exists() returned None, but user exists in the database"
    assert found_user.email == "existing@example.com"


@pytest.mark.asyncio
async def test_username_exists_not_found(mock_db, mocker):
    """
    Test `username_exists()` when the user does not exist.

    Expected Outcome:
    - The function should return None when the username is not found.
    """
    # Ensure database setup works by calling the working function
    await test_ensure_super_admin_exists(mock_db, mocker)

    # Verify that no user exists before calling `username_exists()`
    assert (
        await User.find_one(User.email == "nonexistent@example.com") is None
    ), "User should not exist before test"

    # Run `username_exists()` and verify it returns None
    found_user = await username_exists("nonexistent@example.com")
    assert (
        found_user is None
    ), "username_exists() should return None for a non-existent user"
