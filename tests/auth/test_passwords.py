"""
test_passwords.py

Unit tests for the password hashing and verification module in the JANUX Authentication Gateway.

Tests:
- Secure password hashing
- Password verification for matching and non-matching passwords
- Handling of invalid password inputs
- Empty password edge cases
- Mocking bcrypt operations for efficiency

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from unittest.mock import patch
from janux_auth_gateway.auth.passwords import hash_password, verify_password


def test_hash_password():
    """
    Test that password hashing produces a valid bcrypt hash.

    Expected Outcome:
    - The returned hash should be a non-empty string.
    - The hash should start with a bcrypt prefix ($2b$).
    """
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$")
    assert len(hashed) > 30  # Ensuring it's a valid bcrypt hash length


def test_verify_password():
    """
    Test that password verification correctly matches a valid hash.

    Expected Outcome:
    - The function should return True for matching passwords.
    - The function should return False for incorrect passwords.
    """
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True  # Correct password
    assert verify_password("WrongPassword!", hashed) is False  # Incorrect password


def test_invalid_password_types():
    """
    Test handling of invalid input types for hashing.

    Expected Outcome:
    - Function should raise ValueError for non-string inputs.
    """
    with pytest.raises(ValueError):
        hash_password(12345)  # Non-string input

    with pytest.raises(ValueError):
        hash_password(None)  # None as input

    with pytest.raises(ValueError):
        hash_password(["list", "not", "allowed"])  # List input


def test_empty_password():
    """
    Test that empty or whitespace-only passwords are rejected.

    Expected Outcome:
    - Function should raise ValueError for empty or whitespace-only passwords.
    """
    with pytest.raises(ValueError):
        hash_password("")

    with pytest.raises(ValueError):
        hash_password("     ")  # Only spaces


def test_verify_password_with_invalid_inputs():
    """
    Test handling of invalid input types for verification.

    Expected Outcome:
    - Function should return False if input types are incorrect.
    """
    hashed = hash_password("ValidPassword")

    assert verify_password(12345, hashed) is False  # Non-string input
    assert verify_password(None, hashed) is False  # None as input
    assert verify_password("", hashed) is False  # Empty string


def test_mocked_hash_password(mocker):
    """
    Test password hashing with a mocked bcrypt context.

    Expected Outcome:
    - The function should return a mocked hash without actually performing computation.
    """
    mocker.patch(
        "janux_auth_gateway.auth.passwords.bcrypt_context.hash",
        return_value="mocked_hash",
    )

    hashed = hash_password("MockedPassword")
    assert hashed == "mocked_hash"


def test_mocked_verify_password(mocker):
    """
    Test password verification with a mocked bcrypt context.

    Expected Outcome:
    - The function should return True/False as mocked values.
    """
    mocker.patch(
        "janux_auth_gateway.auth.passwords.bcrypt_context.verify", return_value=True
    )
    assert verify_password("any_password", "mocked_hash") is True

    mocker.patch(
        "janux_auth_gateway.auth.passwords.bcrypt_context.verify", return_value=False
    )
    assert verify_password("wrong_password", "mocked_hash") is False
