"""
test_user.py

Unit tests for the user schemas in the JANUX Authentication Gateway.

Tests:
- Validation of UserBase, UserCreate, UserResponse, and UserLogin schemas.
- Ensuring example values match expected outputs.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from pydantic import ValidationError
from janux_auth_gateway.schemas.user import (
    UserBase,
    UserCreate,
    UserResponse,
    UserLogin,
)


def test_user_base_schema():
    """
    Test the UserBase schema.

    Expected Outcome:
    - The schema should correctly store `email` and `full_name`.
    """
    user = UserBase(email="jane.doe@example.com", full_name="Jane Doe")

    assert user.email == "jane.doe@example.com"
    assert user.full_name == "Jane Doe"


def test_user_create_schema():
    """
    Test the UserCreate schema.

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

    Expected Outcome:
    - Each invalid password should raise a `ValidationError`.
    """
    with pytest.raises(
        ValidationError, match="Password must be at least 8 characters long."
    ):
        UserCreate(email="jane.doe@example.com", full_name="Jane Doe", password="short")

    with pytest.raises(
        ValidationError, match="Password must contain at least one number."
    ):
        UserCreate(
            email="jane.doe@example.com", full_name="Jane Doe", password="NoNumbersHere"
        )

    with pytest.raises(
        ValidationError, match="Password must contain at least one letter."
    ):
        UserCreate(
            email="jane.doe@example.com", full_name="Jane Doe", password="12345678"
        )


def test_user_response_schema():
    """
    Test the UserResponse schema.

    Expected Outcome:
    - The schema should correctly store `id`, `email`, and `full_name`.
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

    Expected Outcome:
    - The schema should correctly store `email` and `password`.
    """
    user = UserLogin(email="jane.doe@example.com", password="Passw0rd123!")

    assert user.email == "jane.doe@example.com"
    assert user.password == "Passw0rd123!"


def test_user_schema_examples():
    """
    Test example values of UserBase, UserCreate, UserResponse, and UserLogin schemas.

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
