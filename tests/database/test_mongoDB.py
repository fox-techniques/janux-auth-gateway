"""
test_mongoDB.py

Unit tests for MongoDB initialization, super admin creation, and authentication.

Tests:
- Ensures `init_db()` correctly sets up the test database.
- Verifies that super admin and tester accounts are created.
- Validates user and admin authentication functions.
- Checks for user and admin existence in the database.

Features:
- Uses `mongomock` for a fully in-memory MongoDB.
- Ensures that inserted test users/admins can be retrieved.
- Uses `AsyncIOMotorClient` to provide a real test database environment.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from janux_auth_gateway.database.mongoDB import (
    init_db,
    create_admin_account,
    create_user_account,
    authenticate_user,
    authenticate_admin,
    username_exists,
    admin_username_exists,
)
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.admin import Admin


@pytest.fixture(scope="function")
async def mock_db(mocker):
    """
    Provides an isolated MongoDB test database.
    Uses a real MongoDB instance instead of mongomock.
    Cleans up test data after each test.
    """
    db_name = f"test_db_{uuid.uuid4().hex}"  # Unique test database for each test
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Use real MongoDB
    test_db = client[db_name]

    # Patch `AsyncIOMotorClient` so `init_db()` uses the test database
    mocker.patch(
        "janux_auth_gateway.database.mongoDB.AsyncIOMotorClient", return_value=client
    )

    # Initialize Beanie models for test database
    await init_beanie(database=test_db, document_models=[User, Admin])

    await test_db["Admin"].create_index([("email", 1)], unique=True)
    await test_db["User"].create_index([("email", 1)], unique=True)

    test_admin = (
        "test.super.admin@example.com",
        "TestSuperAdminPassw0rd123!",
        "Test SuperAdminovski",
        "super_admin",
    )
    test_user = (
        "test.user@example.com",
        "TestUserPassw0rd123!",
        "Test TestUserovski",
        "user",
    )

    # Create default accounts (super admin & tester) in the test database
    await create_admin_account(*test_admin)
    await create_user_account(*test_user)

    yield test_db, test_admin, test_user  # Provide test DB to tests

    # Cleanup: Drop test database after each test
    await client.drop_database(db_name)


@pytest.mark.asyncio
async def test_create_admin_account(mock_db):
    """
    Test creation of an admin account.

    Expected Outcome:
    - A new admin account should be added to the database.
    """
    test_db, test_admin, _ = mock_db
    email, password, full_name, role = test_admin

    # Ensure no admin exists before the test
    assert await Admin.find_one(Admin.email == email) is not None

    # Create an admin account
    await create_admin_account(email, password, full_name=full_name, role=role)

    # Verify that the admin exists in the database
    created_admin = await Admin.find_one(Admin.email == email)
    assert created_admin is not None
    assert created_admin.email == email
    assert created_admin.full_name == full_name
    assert created_admin.role == role


@pytest.mark.asyncio
async def test_create_user_account(mock_db):
    """
    Test creation of a user account.

    Expected Outcome:
    - A new user account should be added to the database.
    """
    test_db, _, test_user = mock_db
    email, password, full_name, role = test_user

    # Ensure no user exists before the test
    assert await User.find_one(User.email == email) is not None

    # Create a user account
    await create_user_account(email, password, full_name=full_name, role=role)

    # Verify that the user exists in the database
    created_user = await User.find_one(User.email == email)
    assert created_user is not None
    assert created_user.email == email
    assert created_user.full_name == full_name
    assert created_user.role == role


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_db):
    """
    Test user authentication with correct credentials.

    Expected Outcome:
    - Authentication should succeed with correct password.
    """
    _, _, test_user = mock_db
    email, password, _, _ = test_user

    assert await authenticate_user(email, password) is True


@pytest.mark.asyncio
async def test_authenticate_user_fail(mock_db):
    """
    Test user authentication failure due to incorrect password.

    Expected Outcome:
    - Authentication should fail with incorrect password.
    """
    _, _, test_user = mock_db
    email, _, _, _ = test_user

    assert await authenticate_user(email, "WrongPass123!") is False


@pytest.mark.asyncio
async def test_authenticate_admin_success(mock_db):
    """
    Test admin authentication with correct credentials.

    Expected Outcome:
    - Authentication should succeed with correct password.
    """
    _, test_admin, _ = mock_db
    email, password, _, _ = test_admin

    assert await authenticate_admin(email, password) is True


@pytest.mark.asyncio
async def test_authenticate_admin_fail(mock_db):
    """
    Test admin authentication failure due to incorrect password.

    Expected Outcome:
    - Authentication should fail with incorrect password.
    """
    _, test_admin, _ = mock_db
    email, _, _, _ = test_admin

    assert await authenticate_admin(email, "WrongPass123!") is False


@pytest.mark.asyncio
async def test_username_exists_found(mock_db):
    """
    Test `username_exists()` when the user exists.

    Expected Outcome:
    - The function should return the user object when the username exists.
    """
    _, _, test_user = mock_db
    email, _, _, _ = test_user

    found_user = await username_exists(email)
    assert found_user is not None
    assert found_user.email == email


@pytest.mark.asyncio
async def test_username_exists_not_found(mock_db):
    """
    Test `username_exists()` when the user does not exist.

    Expected Outcome:
    - The function should return None when the username is not found.
    """
    found_user = await username_exists("nonexistent@example.com")
    assert found_user is None


@pytest.mark.asyncio
async def test_admin_username_exists_found(mock_db):
    """
    Test `admin_username_exists()` when the admin exists.

    Expected Outcome:
    - The function should return the admin object when the admin exists.
    """
    _, test_admin, _ = mock_db
    email, _, _, _ = test_admin

    found_admin = await admin_username_exists(email)
    assert found_admin is not None
    assert found_admin.email == email


@pytest.mark.asyncio
async def test_admin_username_exists_not_found(mock_db):
    """
    Test `admin_username_exists()` when the admin does not exist.

    Expected Outcome:
    - The function should return None when the admin is not found.
    """
    found_admin = await admin_username_exists("nonexistent_admin@example.com")
    assert found_admin is None
