"""
test_jwt.py

Unit tests for the JWT authentication module in the JANUX Authentication Gateway.

Tests:
- JWT access token creation
- JWT decoding for valid and invalid tokens
- Role-based authentication enforcement (user vs admin)
- Handling of expired or malformed tokens

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import time
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError
from janux_auth_gateway.auth.jwt import (
    create_access_token,
    get_current_user,
    get_current_admin,
)
from janux_auth_gateway.config import Config
from fastapi import HTTPException

# Constants for testing
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM


def test_create_access_token():
    """
    Test JWT token creation with and without expiration.

    Steps:
    1. Create a token with default expiration.
    2. Create a token with a custom expiration.
    3. Decode and verify expiration claims.

    Expected Outcome:
    - The generated token should contain the expected payload and expiration.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)

    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_payload["sub"] == "testuser"
    assert decoded_payload["role"] == "user"
    assert "exp" in decoded_payload


def test_create_access_token_with_expiry():
    """
    Test JWT token expiration time.

    Steps:
    1. Create a token with a short expiration (2 seconds).
    2. Sleep for 3 seconds to let it expire.
    3. Attempt to decode the token.

    Expected Outcome:
    - The token should expire and raise an exception.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data, expires_delta=timedelta(seconds=2))

    time.sleep(3)  # Wait for token to expire

    with pytest.raises(JWTError):
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def test_valid_user_token():
    """
    Test decoding a valid user token.

    Steps:
    1. Create a valid user token.
    2. Pass it to `get_current_user()`.

    Expected Outcome:
    - The function should return the correct user information.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)

    user = get_current_user(token)
    assert user["username"] == "testuser"
    assert user["role"] == "user"


def test_valid_admin_token():
    """
    Test decoding a valid admin token.

    Steps:
    1. Create a valid admin token.
    2. Pass it to `get_current_admin()`.

    Expected Outcome:
    - The function should return the correct admin information.
    """
    data = {"sub": "adminuser", "role": "admin"}
    token = create_access_token(data)

    admin = get_current_admin(token)
    assert admin["username"] == "adminuser"
    assert admin["role"] == "admin"


def test_invalid_token():
    """
    Test handling of an invalid JWT token.

    Steps:
    1. Create a corrupted token.
    2. Pass it to `get_current_user()`.

    Expected Outcome:
    - The function should raise an HTTPException for an invalid token.
    """
    invalid_token = "invalid.jwt.token"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(invalid_token)

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


def test_invalid_role():
    """
    Test handling of a token with an incorrect role.

    Steps:
    1. Create a token for a user.
    2. Pass it to `get_current_admin()` (expect failure).

    Expected Outcome:
    - The function should raise an HTTPException because the user role is invalid.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)

    with pytest.raises(HTTPException) as exc_info:
        get_current_admin(token)

    assert exc_info.value.status_code == 401
    assert "Could not validate admin" in exc_info.value.detail


def test_expired_token():
    """
    Test handling of an expired token.

    Steps:
    1. Create a token with a 1-second expiration.
    2. Sleep for 2 seconds to let it expire.
    3. Attempt to decode the token.

    Expected Outcome:
    - The function should raise an HTTPException due to expiration.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data, expires_delta=timedelta(seconds=1))

    time.sleep(2)  # Let the token expire

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token)

    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail
