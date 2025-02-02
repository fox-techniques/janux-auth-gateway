"""
test_passwords.py

Unit tests for the password management module in the JANUX Authentication Gateway.

Tests:
- Password complexity enforcement.
- Secure password hashing.
- Password verification.
- Rate-limiting for failed password attempts.
- Hash upgrading.

Features:
- Uses `fakeredis` for an in-memory Redis instance.
- Mocks `Passlib CryptContext` for password hashing.
- Ensures rate-limiting prevents brute-force attacks.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import fakeredis
from unittest.mock import patch
from fastapi import HTTPException
from passlib.context import CryptContext
from janux_auth_gateway.auth.passwords import (
    is_password_secure,
    hash_password,
    verify_password,
    upgrade_password_hash,
)


@pytest.fixture()
def fake_redis():
    """
    Creates an in-memory Redis instance for testing.
    """
    return fakeredis.FakeRedis(decode_responses=True)


@pytest.fixture()
def mock_password_context(mocker):
    """
    Mocks the Passlib CryptContext to avoid real hashing in tests.
    """
    mock_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    mocker.patch("janux_auth_gateway.auth.passwords.bcrypt_context", mock_context)
    return mock_context


@pytest.fixture()
def strong_password():
    """
    Returns a strong password that meets security requirements.
    """
    return "StrongP@ssw0rd!"


def test_is_password_secure():
    """
    Test that password complexity rules are enforced correctly.

    Expected Outcome:
    - Secure passwords return True.
    - Weak passwords return False.
    """
    assert is_password_secure("ValidP@ss1") is True
    assert is_password_secure("weak") is False
    assert is_password_secure("NoNumbers!") is False
    assert is_password_secure("nocapital1!") is False
    assert is_password_secure("NOLOWERCASE1!") is False
    assert is_password_secure("NoSpecialChar1") is False


def test_hash_password(mock_password_context, strong_password):
    """
    Test password hashing using bcrypt or argon2.

    Expected Outcome:
    - Returns a valid hashed password with an expected prefix.
    """
    hashed = hash_password(strong_password)
    assert isinstance(hashed, str)

    # Dynamically check for any supported hashing scheme
    valid_schemes = ["$argon2", "$bcrypt", "$2b$"]
    assert any(
        hashed.startswith(scheme) for scheme in valid_schemes
    ), f"Unexpected hash format: {hashed}"


def test_hash_password_fails_on_weak_password():
    """
    Test that weak passwords raise a ValueError.

    Expected Outcome:
    - Raises ValueError if password is too weak.
    """
    with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
        hash_password("weak")


def test_verify_password_success(mock_password_context, fake_redis, strong_password):
    """
    Test successful password verification.

    Expected Outcome:
    - Returns True when the correct password is provided.
    """
    hashed_password = hash_password(strong_password)
    assert (
        verify_password(
            strong_password,
            hashed_password,
            "user@example.com",
            redis_client=fake_redis,
        )
        is True
    )


def test_verify_password_failure(mock_password_context, fake_redis, strong_password):
    """
    Test failed password verification.

    Expected Outcome:
    - Returns False when an incorrect password is provided.
    """
    hashed_password = hash_password(strong_password)
    assert (
        verify_password(
            "WrongPass!",
            hashed_password,
            "user@example.com",
            redis_client=fake_redis,
        )
        is False
    )


def test_verify_password_rate_limit(mock_password_context, fake_redis, strong_password):
    """
    Test rate-limiting on failed password attempts.

    Expected Outcome:
    - After 5 failed attempts, raises HTTPException (429 Too Many Requests).
    """
    hashed_password = hash_password(strong_password)
    user_id = "user@example.com"

    for _ in range(5):
        verify_password("WrongPass!", hashed_password, user_id, redis_client=fake_redis)

    with pytest.raises(HTTPException, match="Too many login attempts"):
        verify_password("WrongPass!", hashed_password, user_id, redis_client=fake_redis)


def test_upgrade_password_hash(mock_password_context, strong_password):
    """
    Test upgrading password hashes.

    Expected Outcome:
    - Returns an upgraded hash if the old one is outdated.
    - Returns the same hash if it's already secure.
    """
    old_hash = hash_password(strong_password)
    assert upgrade_password_hash(strong_password, old_hash) == old_hash
