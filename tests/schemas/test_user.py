"""
test_user.py

Unit tests for the user-related schemas in the JANUX Authentication Gateway.

Tests:
- Validation of UserBase schema.
- Validation of UserCreate schema.
- Password validation enforcement.
- Validation of UserResponse schema.
- Validation of UserLogin schema.
- Ensuring example values match expected outputs.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from janux_auth_gateway.schemas.user import (
    UserBase,
    UserCreate,
    UserResponse,
    UserLogin,
)


def test_user_base_schema():
    """
    Test the UserBase schema.

    Steps:
    1. Create a `UserBase` instance.
    2. Verify that it correctly stores `email` and `full_name`.

    Expected Outcome:
    - The schema should correctly store user details.
    """
    user = UserBase(email="jane.doe@example.com", full_name="Jane Doe")

    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"


def test_user_create_schema():
    """
    Test the UserCreate schema.

    Steps:
    1. Create a `UserCreate` instance with a valid password.
    2. Verify that it correctly stores the data.

    Expected Outcome:
    - The schema should correctly store user details, including password.
    """
    user = UserCreate(
        email="jane.doe@example.com", full_name="Jane Doe", password="Passw0rd123!"
    )

    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"
    assert user.password == "Passw0rd123!"


def test_user_create_password_validation():
    """
    Test password validation in UserCreate schema.

    Steps:
    1. Attempt to create `UserCreate` instances with invalid passwords.

    Expected Outcome:
    - Each invalid password should raise a `ValueError`.
    """
    with pytest.raises(
        ValueError, match="Password must be at least 8 characters long."
    ):
        UserCreate(email="jane.doe@example.com", full_name="Jane Doe", password="short")

    with pytest.raises(ValueError, match="Password must contain at least one number."):
        UserCreate(
            email="jane.doe@example.com", full_name="Jane Doe", password="NoNumbersHere"
        )

    with pytest.raises(ValueError, match="Password must contain at least one letter."):
        UserCreate(
            email="jane.doe@example.com", full_name="Jane Doe", password="12345678"
        )


def test_user_response_schema():
    """
    Test the UserResponse schema.

    Steps:
    1. Create a `UserResponse` instance.
    2. Verify that it correctly stores `id`, `email`, and `full_name`.

    Expected Outcome:
    - The schema should correctly store response data.
    """
    user = UserResponse(
        id="507f1f77bcf86cd799439011",
        email="jane.doe@example.com",
        full_name="Jane Doe",
    )

    assert user.id == "507f1f77bcf86cd799439011"
    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"


def test_user_login_schema():
    """
    Test the UserLogin schema.

    Steps:
    1. Create a `UserLogin` instance.
    2. Verify that it correctly stores `email` and `password`.

    Expected Outcome:
    - The schema should correctly store login credentials.
    """
    user = UserLogin(email="jane.doe@example.com", password="Passw0rd123!")

    assert user.email == "jane.doe@example.com"
    assert user.password == "Passw0rd123!"


def test_user_schema_examples():
    """
    Test example values of UserBase, UserCreate, UserResponse, and UserLogin schemas.

    Steps:
    1. Retrieve schema examples for each user-related schema.
    2. Verify they match the expected values.

    Expected Outcome:
    - The example values should match the expected schema examples.
    """
    base_example = UserBase.model_json_schema()["properties"]
    create_example = UserCreate.model_json_schema()["properties"]
    response_example = UserResponse.model_json_schema()["properties"]
    login_example = UserLogin.model_json_schema()["properties"]

    assert base_example["email"]["example"] == "jane.doe@example.com"
    assert base_example["full_name"]["example"] == "Jane Doe"

    assert create_example["password"]["example"] == "Passw0rd123!"
    assert response_example["id"]["example"] == "507f1f77bcf86cd799439011"

    assert login_example["email"]["example"] == "jane.doe@example.com"
    assert login_example["password"]["example"] == "Passw0rd123!"
