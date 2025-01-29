"""
test_user.py

Unit tests for the User model in the JANUX Authentication Gateway.

Tests:
- Validation of required fields.
- Ensuring `created_at` is set correctly.
- Database insert and retrieval operations.
- Enforcing unique email constraints.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from datetime import datetime, timezone
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.roles import UserRole


def test_user_valid_data():
    """
    Test creating a User instance with valid data.

    Steps:
    1. Create a `User` instance with valid attributes.

    Expected Outcome:
    - The instance should be created successfully.
    """
    user = User(
        email="jane.doe@example.com",
        full_name="Jane Doe",
        hashed_password="hashedpassword123",
        role=UserRole.CONTRIBUTOR,
    )

    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"
    assert user.hashed_password == "hashedpassword123"
    assert user.role == UserRole.CONTRIBUTOR
    assert isinstance(user.created_at, datetime)
    assert user.created_at <= datetime.now(timezone.utc)  # Ensure it's set


def test_user_invalid_full_name():
    """
    Test validation of the full name field.

    Steps:
    1. Attempt to create a `User` instance with an empty full name.

    Expected Outcome:
    - The function should raise a `ValueError`.
    """
    with pytest.raises(ValueError, match="Full name cannot be empty."):
        User(
            email="jane.doe@example.com",
            full_name="",
            hashed_password="hashedpassword123",
            role=UserRole.USER,
        )


@pytest.mark.asyncio
async def test_user_database_insert_and_retrieve():
    """
    Test inserting and retrieving a User document from MongoDB.

    Steps:
    1. Create and insert a `User` document.
    2. Retrieve it from the database.

    Expected Outcome:
    - The retrieved user should match the inserted data.
    """
    user = User(
        email="jane.doe@example.com",
        full_name="Jane Doe",
        hashed_password="hashedpassword123",
        role=UserRole.USER,
    )

    await user.insert()
    retrieved_user = await User.find_one(User.email == "jane.doe@example.com")

    assert retrieved_user is not None
    assert retrieved_user.email == "jane.doe@example.com"
    assert retrieved_user.full_name == "Jane Doe"
    assert retrieved_user.role == UserRole.USER


@pytest.mark.asyncio
async def test_user_unique_email_constraint():
    """
    Test enforcing the unique email constraint.

    Steps:
    1. Insert a User document with a specific email.
    2. Attempt to insert another User with the same email.

    Expected Outcome:
    - The second insert should fail due to the unique constraint.
    """
    user1 = User(
        email="unique@example.com",
        full_name="Unique User",
        hashed_password="hashedpassword123",
        role=UserRole.USER,
    )
    await user1.insert()

    user2 = User(
        email="unique@example.com",  # Duplicate email
        full_name="Another User",
        hashed_password="anotherpassword123",
        role=UserRole.USER,
    )

    with pytest.raises(Exception):  # Beanie should enforce uniqueness
        await user2.insert()
