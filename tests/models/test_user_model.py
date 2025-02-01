"""
test_user.py

Unit tests for the User model in the JANUX Authentication Gateway.

Tests:
- User model validation (email, full name, hashed password, role).
- User creation via Beanie.
- Database operations for user insertion and retrieval.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from janux_auth_gateway.models.admin_model import Admin
from janux_auth_gateway.models.user_model import User
from janux_auth_gateway.models.roles_model import UserRole
from janux_auth_gateway.database.mongoDB import create_user_account


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

    yield test_db  # Provide test DB to tests

    # Cleanup: Drop test database after each test
    await client.drop_database(db_name)


@pytest.mark.asyncio
async def test_user_model_success(mock_db):
    """
    Test that a valid User model is created successfully.

    Expected Outcome:
    - The model should be instantiated without errors.
    """
    user = User(
        email="test.user@example.com",
        full_name="Test User",
        hashed_password="hashed_password_123",
        role=UserRole.USER,
        created_at=datetime(2025, 1, 23, 12, 0, 0, tzinfo=timezone.utc),
    )

    assert user.email == "test.user@example.com"
    assert user.full_name == "Test User"
    assert user.hashed_password == "hashed_password_123"
    assert user.role == UserRole.USER
    assert user.created_at == datetime(2025, 1, 23, 12, 0, 0, tzinfo=timezone.utc)


@pytest.mark.asyncio
async def test_user_creation_via_db_function(mock_db):
    """
    Test creating a user via the `create_user_account` function.

    Expected Outcome:
    - The function should create a user in the database.
    """
    email = "test.user@example.com"
    password = "TestUserPassword123!"
    full_name = "Test Userovski"
    role = "user"  # Must be one of the allowed values in UserRole

    await create_user_account(
        email=email, password=password, full_name=full_name, role=role
    )

    saved_user = await User.find_one(User.email == email)

    assert saved_user is not None
    assert saved_user.email == email
    assert saved_user.full_name == full_name
    assert saved_user.role == role  # Ensure correct role is saved


@pytest.mark.asyncio
async def test_user_model_invalid_full_name(mock_db):
    """
    Test that an empty or too short full name raises a validation error.

    Expected Outcome:
    - Pydantic validation should raise a ValueError.
    """
    with pytest.raises(ValueError, match="should have at least 3 characters"):

        await User(
            email="test.user@example.com",
            full_name="A",
            hashed_password="hashed_password_123",
            role=UserRole.USER,
        ).insert()


@pytest.mark.asyncio
async def test_user_model_invalid_password(mock_db):
    """
    Test that a password shorter than 8 characters raises a validation error.

    Expected Outcome:
    - Pydantic validation should raise a ValueError.
    """
    with pytest.raises(ValueError, match="should have at least 8 characters"):
        await User(
            email="test.user@example.com",
            full_name="Test User",
            hashed_password="short",
            role=UserRole.USER,
        ).insert()


@pytest.mark.asyncio
async def test_user_unique_email_constraint(mock_db):
    """
    Test enforcing the unique email constraint.

    Expected Outcome:
    - The second insert should fail due to the unique constraint.
    """
    email = "unique.user@example.com"
    full_name = "Unique User"
    password = "SecurePassword123!"

    user1 = User(
        email=email, full_name=full_name, hashed_password=password, role=UserRole.USER
    )
    await user1.insert()

    user2 = User(
        email=email,
        full_name="Another User",
        hashed_password=password,
        role=UserRole.USER,
    )

    with pytest.raises(Exception):  # Beanie should enforce uniqueness
        await user2.insert()
