"""
test_passwords.py

Unit tests for the password hashing and verification module in the JANUX Authentication Gateway.

Tests:
- Hashing passwords securely with bcrypt.
- Ensuring different hashes for the same password (bcrypt randomness).
- Verifying correct and incorrect password matches.
- Handling invalid input cases.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
from janux_auth_gateway.auth.passwords import hash_password, verify_password


def test_hash_password():
    """
    Test hashing a valid password.

    Steps:
    1. Hash a valid password.
    2. Ensure the hashed password is a non-empty string.

    Expected Outcome:
    - The function should return a hashed string.
    """
    password = "securepassword123"
    hashed = hash_password(password)

    assert isinstance(hashed, str)
    assert hashed.startswith("$2b$")  # bcrypt hashes start with $2b$ or similar


def test_hash_password_is_unique():
    """
    Test that hashing the same password twice produces different results.

    Steps:
    1. Hash the same password twice.
    2. Compare the hashed values.

    Expected Outcome:
    - The hashes should be different due to bcrypt's salt mechanism.
    """
    password = "securepassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_hash_password_invalid_input():
    """
    Test that hashing an invalid input raises a ValueError.

    Steps:
    1. Attempt to hash a non-string value (integer).
    2. Attempt to hash an empty string.

    Expected Outcome:
    - The function should raise a ValueError.
    """
    with pytest.raises(ValueError):
        hash_password(123456)  # Non-string input

    with pytest.raises(ValueError):
        hash_password("")  # Empty string


def test_verify_correct_password():
    """
    Test verifying a correct password against a hashed password.

    Steps:
    1. Hash a password.
    2. Verify it against the correct plain-text password.

    Expected Outcome:
    - The function should return True.
    """
    password = "mypassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_incorrect_password():
    """
    Test verifying an incorrect password against a hashed password.

    Steps:
    1. Hash a password.
    2. Attempt verification with an incorrect password.

    Expected Outcome:
    - The function should return False.
    """
    password = "mypassword"
    hashed = hash_password(password)

    assert verify_password("wrongpassword", hashed) is False


def test_verify_password_invalid_input():
    """
    Test handling invalid inputs in password verification.

    Steps:
    1. Attempt verification with non-string inputs.
    2. Attempt verification with empty strings.

    Expected Outcome:
    - The function should return False.
    """
    hashed = hash_password("validpassword")

    assert verify_password(12345, hashed) is False  # Non-string password
    assert verify_password("validpassword", None) is False  # None as hashed password
    assert verify_password("", hashed) is False  # Empty string password
    assert verify_password("validpassword", "") is False  # Empty string hash
