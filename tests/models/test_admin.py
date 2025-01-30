"""
test_admin.py

Unit tests for the Admin model in the JANUX Authentication Gateway.

Tests:
- Admin model initialization.
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
from janux_auth_gateway.models.admin import Admin
from janux_auth_gateway.models.roles import AdminRole
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
    await init_beanie(database=test_db, document_models=[Admin])

    yield test_db  # Provide test DB to tests

    # Cleanup: Drop test database after each test
    await client.drop_database(db_name)


@pytest.mark.asyncio
async def test_admin_model_initialization(mock_db):
    """
    Test the initialization of the Admin model with valid data.

    Expected Outcome:
    - An Admin instance should be created successfully.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashed_password_123",
        role=AdminRole.SUPER_ADMIN,
    )

    assert admin.email == "admin@example.com"
    assert admin.full_name == "Admin User"
    assert admin.hashed_password == "hashed_password_123"
    assert admin.role == AdminRole.SUPER_ADMIN
    assert admin.created_at is not None


def test_admin_full_name_validation():
    """
    Test validation of the full name field.

    Expected Outcome:
    - A `ValidationError` should be raised if the full name is empty or too short.
    """
    with pytest.raises(
        ValidationError, match="String should have at least 3 characters"
    ):
        Admin(
            email="admin@example.com",
            full_name="",
            hashed_password="hashed_password_123",
        )

    with pytest.raises(
        ValidationError, match="String should have at least 3 characters"
    ):
        Admin(
            email="admin@example.com",
            full_name="A",
            hashed_password="hashed_password_123",
        )


def test_admin_password_validation():
    """
    Test validation of the hashed password field.

    Expected Outcome:
    - A `ValidationError` should be raised if the password is too short.
    """
    with pytest.raises(
        ValidationError, match="String should have at least 8 characters"
    ):
        Admin(
            email="admin@example.com", full_name="Admin User", hashed_password="short"
        )


@pytest.mark.asyncio
async def test_admin_database_insert_and_retrieve(mock_db):
    """
    Test inserting and retrieving an Admin document from MongoDB.

    Expected Outcome:
    - The inserted admin should be retrievable from the database.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password=hash_password("securepassword"),
        role=AdminRole.ADMIN,
    )

    await admin.insert()
    retrieved_admin = await Admin.find_one(Admin.email == "admin@example.com")

    assert retrieved_admin is not None
    assert retrieved_admin.email == "admin@example.com"
    assert retrieved_admin.full_name == "Admin User"
    assert retrieved_admin.role == AdminRole.ADMIN
