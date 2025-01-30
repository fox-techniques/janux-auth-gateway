"""
test_admin.py

Unit tests for the Admin model in MongoDB using Beanie.

Tests:
- Admin model creation and validation
- Database persistence and retrieval
- Unique email constraint enforcement
- Default field values

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from datetime import datetime, timezone
from pydantic import ValidationError
from janux_auth_gateway.models.admin import Admin
from janux_auth_gateway.models.roles import AdminRole


@pytest.fixture(scope="function")
async def mock_db():
    """
    Provides a fully in-memory MongoDB for testing.
    Ensures Beanie is initialized with a fresh state before each test.
    """
    db_name = f"test_db"  # Unique DB name per test
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # In-memory MongoDB
    test_db = client[db_name]

    # Initialize Beanie models
    await init_beanie(database=test_db, document_models=[Admin])

    return test_db


@pytest.mark.asyncio
async def test_admin_model_creation(mock_db):
    """
    Test that an Admin instance can be created with valid data.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashedpassword123",
        role=AdminRole.SUPER_ADMIN,
    )

    assert admin.email == "admin@example.com"
    assert admin.full_name == "Admin User"
    assert admin.hashed_password == "hashedpassword123"
    assert admin.role == AdminRole.SUPER_ADMIN
    assert isinstance(admin.created_at, datetime)


@pytest.mark.asyncio
async def test_admin_save_and_retrieve(mock_db):
    """
    Test that an Admin instance is correctly saved to and retrieved from the database.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashedpassword123",
        role=AdminRole.ADMIN,
    )
    await admin.save()

    # Retrieve from database
    retrieved_admin = await Admin.find_one(Admin.email == "admin@example.com")
    assert retrieved_admin is not None
    assert retrieved_admin.email == "admin@example.com"
    assert retrieved_admin.full_name == "Admin User"


@pytest.mark.asyncio
async def test_admin_email_uniqueness(mock_db):
    """
    Test that inserting an admin with a duplicate email raises an error.
    """
    # Ensure the index exists before testing
    indexes = await mock_db["admins"].index_information()
    assert any(
        "email_1" in idx for idx in indexes
    ), "Unique index on email was not created"

    admin1 = Admin(
        email="duplicate@example.com",
        full_name="Admin One",
        hashed_password="hashedpassword1",
        role=AdminRole.ADMIN,
    )
    await admin1.save()

    # Attempt to insert duplicate
    admin2 = Admin(
        email="duplicate@example.com",
        full_name="Admin Two",
        hashed_password="hashedpassword2",
        role=AdminRole.ADMIN,
    )

    # Unique index should enforce constraint, causing an error
    with pytest.raises(Exception, match="E11000 duplicate key error collection"):
        await admin2.save()


@pytest.mark.asyncio
async def test_admin_default_role(mock_db):
    """
    Test that the default role is set to `admin` if not provided.
    """
    admin = Admin(
        email="defaultrole@example.com",
        full_name="Admin Default",
        hashed_password="hashedpassword123",
    )
    await admin.save()

    retrieved_admin = await Admin.find_one(Admin.email == "defaultrole@example.com")
    assert retrieved_admin is not None
    assert retrieved_admin.role == AdminRole.ADMIN


@pytest.mark.asyncio
async def test_admin_default_created_at(mock_db):
    """
    Test that `created_at` defaults to the current UTC timestamp.
    """
    before_insert = datetime.now(timezone.utc)
    admin = Admin(
        email="timecheck@example.com",
        full_name="Admin Time",
        hashed_password="hashedpassword123",
    )
    await admin.save()

    retrieved_admin = await Admin.find_one(Admin.email == "timecheck@example.com")
    assert retrieved_admin is not None
    assert before_insert <= retrieved_admin.created_at <= datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_admin_missing_required_fields(mock_db):
    """
    Test that creating an Admin instance with missing required fields raises validation errors.
    """
    with pytest.raises(ValidationError, match="full_name"):
        Admin(
            email="missingname@example.com",
            hashed_password="hashedpassword123",
        )

    with pytest.raises(ValidationError, match="email"):
        Admin(
            full_name="Missing Email",
            hashed_password="hashedpassword123",
        )

    with pytest.raises(ValidationError, match="hashed_password"):
        Admin(
            email="missingpassword@example.com",
            full_name="Missing Password",
        )


@pytest.mark.asyncio
async def test_admin_full_name_validation(mock_db):
    """
    Test that an empty `full_name` field raises a validation error.
    """
    with pytest.raises(ValueError, match="Full name cannot be empty"):
        Admin(
            email="invalidname@example.com",
            full_name="",
            hashed_password="hashedpassword123",
        )
