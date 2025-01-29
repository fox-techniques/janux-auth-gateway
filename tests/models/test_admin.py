"""
test_admin.py

Unit tests for the Admin model in the JANUX Authentication Gateway.

Tests:
- Validation of required fields.
- Ensuring `created_at` is set correctly.
- Database insert and retrieval operations.
- Enforcing unique email constraints.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from datetime import datetime, timezone
from janux_auth_gateway.models.admin import Admin
from janux_auth_gateway.models.roles import AdminRole


def test_admin_valid_data():
    """
    Test creating an Admin instance with valid data.

    Steps:
    1. Create an `Admin` instance with valid attributes.

    Expected Outcome:
    - The instance should be created successfully.
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
    assert admin.created_at <= datetime.now(timezone.utc)  # Ensure it's set


def test_admin_invalid_full_name():
    """
    Test validation of the full name field.

    Steps:
    1. Attempt to create an `Admin` instance with an empty full name.

    Expected Outcome:
    - The function should raise a `ValueError`.
    """
    with pytest.raises(ValueError, match="Full name cannot be empty."):
        Admin(
            email="admin@example.com",
            full_name="",
            hashed_password="hashedpassword123",
            role=AdminRole.ADMIN,
        )


@pytest.mark.asyncio
async def test_admin_database_insert_and_retrieve():
    """
    Test inserting and retrieving an Admin document from MongoDB.

    Steps:
    1. Create and insert an `Admin` document.
    2. Retrieve it from the database.

    Expected Outcome:
    - The retrieved admin should match the inserted data.
    """
    admin = Admin(
        email="admin@example.com",
        full_name="Admin User",
        hashed_password="hashedpassword123",
        role=AdminRole.ADMIN,
    )

    await admin.insert()
    retrieved_admin = await Admin.find_one(Admin.email == "admin@example.com")

    assert retrieved_admin is not None
    assert retrieved_admin.email == "admin@example.com"
    assert retrieved_admin.full_name == "Admin User"
    assert retrieved_admin.role == AdminRole.ADMIN


@pytest.mark.asyncio
async def test_admin_unique_email_constraint():
    """
    Test enforcing the unique email constraint.

    Steps:
    1. Insert an Admin document with a specific email.
    2. Attempt to insert another Admin with the same email.

    Expected Outcome:
    - The second insert should fail due to the unique constraint.
    """
    admin1 = Admin(
        email="unique@example.com",
        full_name="Unique Admin",
        hashed_password="hashedpassword123",
        role=AdminRole.ADMIN,
    )
    await admin1.insert()

    admin2 = Admin(
        email="unique@example.com",  # Duplicate email
        full_name="Another Admin",
        hashed_password="anotherpassword123",
        role=AdminRole.ADMIN,
    )

    with pytest.raises(Exception):  # Beanie should enforce uniqueness
        await admin2.insert()
