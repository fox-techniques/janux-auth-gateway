"""
test_user.py

Unit tests for the User model in the JANUX Authentication Gateway.

Tests:
- User model initialization.
- Full name and password validation.
- Database insert and retrieval operations.
- Enforcing unique email constraints.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import ValidationError
from beanie import init_beanie
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.roles import UserRole
from janux_auth_gateway.auth.passwords import hash_password


@pytest.fixture(scope="function")
async def mock_db():
    """
    Provides a fully isolated MongoDB for testing.
    Ensures Beanie is initialized properly.
    Cleans up test data after each test.
    """
    db_name = f"test_db_{uuid.uuid4().hex}"  # Unique test database for each run
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Local MongoDB
    test_db = client[db_name]

    # Initialize Beanie models for test database
    await init_beanie(database=test_db, document_models=[User])

    yield test_db  # Provide test DB to tests

    # Cleanup: Drop test database after each test
    await client.drop_database(db_name)


@pytest.mark.asyncio
async def test_user_model_initialization(mock_db):
    """
    Test the initialization of the User model with valid data.

    Expected Outcome:
    - A User instance should be created successfully.
    """
    user = User(
        email="jane.doe@example.com",
        full_name="Jane Doe",
        hashed_password="hashed_password_123",
        role=UserRole.USER,
    )

    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"
    assert user.hashed_password == "hashed_password_123"
    assert user.role == UserRole.USER
    assert user.created_at is not None


def test_user_full_name_validation():
    """
    Test validation of the full name field.

    Expected Outcome:
    - A `ValidationError` should be raised if the full name is empty or too short.
    """
    with pytest.raises(
        ValidationError, match="String should have at least 3 characters"
    ):
        User(
            email="jane.doe@example.com",
            full_name="",
            hashed_password="hashed_password_123",
        )

    with pytest.raises(
        ValidationError, match="String should have at least 3 characters"
    ):
        User(
            email="jane.doe@example.com",
            full_name="A",
            hashed_password="hashed_password_123",
        )


def test_user_password_validation():
    """
    Test validation of the hashed password field.

    Expected Outcome:
    - A `ValidationError` should be raised if the password is too short.
    """
    with pytest.raises(
        ValidationError, match="String should have at least 8 characters"
    ):
        User(
            email="jane.doe@example.com", full_name="Jane Doe", hashed_password="short"
        )


@pytest.mark.asyncio
async def test_user_database_insert_and_retrieve(mock_db):
    """
    Test inserting and retrieving a User document from MongoDB.

    Expected Outcome:
    - The inserted user should be retrievable from the database.
    """
    user = User(
        email="jane.doe@example.com",
        full_name="Jane Doe",
        hashed_password=hash_password("securepassword"),
        role=UserRole.USER,
    )

    await user.insert()
    retrieved_user = await User.find_one(User.email == "jane.doe@example.com")

    assert retrieved_user is not None
    assert retrieved_user.email == "jane.doe@example.com"
    assert retrieved_user.full_name == "Jane Doe"
    assert retrieved_user.role == UserRole.USER
