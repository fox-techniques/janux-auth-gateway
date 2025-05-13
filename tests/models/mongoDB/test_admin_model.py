"""
test_admin.py

Unit tests for the Admin model in the JANUX Authentication Gateway.

Tests:
- Successful Admin model creation.
- Validation errors for invalid email, short full_name, and short hashed_password.
- Ensures invalid roles are rejected.
- Confirms the __str__() representation.


Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import uuid
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from janux_auth_gateway.models.mongoDB.admin_model import Admin
from janux_auth_gateway.models.mongoDB.roles_model import AdminRole
from janux_auth_gateway.models.mongoDB.user_model import User
from janux_auth_gateway.database.mongoDB import create_admin_account


@pytest.fixture()
@pytest.mark.asyncio(loop_scope="function")
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


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_model_success(mock_db):
    """
    Test that a valid Admin model is created successfully.

    Expected Outcome:
    - The model should be instantiated without errors and inserted into the DB.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashed_password_123",
        role=AdminRole.ADMIN,
        created_at=datetime(2025, 1, 23, 12, 0, 0, tzinfo=timezone.utc),
    )

    await admin.insert()
    saved_admin = await Admin.find_one(Admin.email == "admin@example.com")

    assert saved_admin is not None
    assert saved_admin.email == admin.email
    assert saved_admin.full_name == admin.full_name
    assert saved_admin.role == admin.role


@pytest.mark.asyncio
async def test_admin_invalid_email(mock_db):
    """
    Test that an invalid email raises a validation error.

    Expected Outcome:
    - A ValidationError should be raised for an invalid email format.
    """
    with pytest.raises(ValueError):
        await Admin(
            email="invalid-email",
            full_name="Admin User",
            hashed_password="hashed_password_123",
            role=AdminRole.ADMIN,
        ).insert()


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_short_full_name(mock_db):
    """
    Test that a short full name raises a validation error.

    Expected Outcome:
    - A ValidationError should be raised if full_name is shorter than 3 characters.
    """
    with pytest.raises(ValueError):
        await Admin(
            email="admin@example.com",
            full_name="A",
            hashed_password="hashed_password_123",
            role=AdminRole.ADMIN,
        ).insert()


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_short_password(mock_db):
    """
    Test that a short hashed password raises a validation error.

    Expected Outcome:
    - A ValidationError should be raised if the password is shorter than 8 characters.
    """
    with pytest.raises(ValueError):
        await Admin(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password="short",
            role=AdminRole.ADMIN,
        ).insert()


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_invalid_role(mock_db):
    """
    Test that an invalid role raises a validation error.

    Expected Outcome:
    - A ValidationError should be raised if an invalid role is provided.
    """
    with pytest.raises(ValueError):
        await Admin(
            email="admin@example.com",
            full_name="Admin User",
            hashed_password="hashed_password_123",
            role="invalid_role",
        ).insert()


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_creation_via_db_function(mock_db):
    """
    Test creating an admin via the `create_admin_account` function.

    Expected Outcome:
    - The function should create an admin in the database.
    """
    email = "test.admin@example.com"
    password = "TestSuperAdmin123!"
    full_name = "Test Adminovski"
    role = "super_admin"

    await create_admin_account(
        email=email, password=password, full_name=full_name, role=role
    )

    saved_admin = await Admin.find_one(Admin.email == email)

    assert saved_admin is not None
    assert saved_admin.email == email
    assert saved_admin.full_name == full_name
    assert saved_admin.role == role


@pytest.mark.asyncio(loop_scope="function")
async def test_admin_str_representation(mock_db):
    """
    Test the string representation of the Admin model.

    Expected Outcome:
    - The __str__() method should return the correct format.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashed_password_123",
        role=AdminRole.ADMIN,
        created_at=datetime(2025, 1, 23, 12, 0, 0, tzinfo=timezone.utc),
    )

    expected_str = (
        f"Admin(email={admin.email}, role={admin.role}, created_at={admin.created_at})"
    )
    assert str(admin) == expected_str
