"""
test_jwt.py

Unit tests for the JWT authentication module in the JANUX Authentication Gateway.

Tests:
- JWT access token creation
- JWT decoding for valid and invalid tokens
- Role-based authentication enforcement (user vs admin)
- Handling of expired or malformed tokens

Replaced python-jose with PyJWT for enhanced security.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import secrets
from datetime import timedelta, datetime, timezone
import jwt
from fastapi import HTTPException
from unittest.mock import patch
from freezegun import freeze_time

from janux_auth_gateway.auth.jwt import (
    create_access_token,
    verify_jwt,
    get_current_user,
    get_current_admin,
)
from janux_auth_gateway.config import Config

# Mocked constants
MOCK_SECRET_KEY = secrets.token_urlsafe(32)
MOCK_ALGORITHM = "RS256"


@pytest.fixture(autouse=True)
def mock_config_env(mocker):
    """Mock Config to prevent using real secrets"""
    mocker.patch.object(Config, "SECRET_KEY", MOCK_SECRET_KEY)
    mocker.patch.object(Config, "ALGORITHM", MOCK_ALGORITHM)
    mocker.patch.object(Config, "ACCESS_TOKEN_EXPIRE_MINUTES", 20)


def test_create_access_token():
    """
    Test JWT token creation with a default expiration.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)
    decoded_payload = verify_jwt(token)
    assert decoded_payload["sub"] == "testuser"
    assert decoded_payload["role"] == "user"
    assert "exp" in decoded_payload


def test_create_access_token_with_expiry():
    """
    Test JWT token expiration time.
    """
    data = {"sub": "testuser", "role": "user"}
    with freeze_time(datetime.now(timezone.utc)) as frozen_time:
        token = create_access_token(data, expires_delta=timedelta(seconds=2))
        frozen_time.tick(delta=timedelta(seconds=3))
        with pytest.raises(HTTPException):
            verify_jwt(token)


def test_valid_user_token():
    """
    Test decoding a valid user token.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)
    user = get_current_user(token)
    assert user["username"] == "testuser"
    assert user["role"] == "user"


def test_valid_admin_token():
    """
    Test decoding a valid admin token.
    """
    data = {"sub": "adminuser", "role": "admin"}
    token = create_access_token(data)
    admin = get_current_admin(token)
    assert admin["username"] == "adminuser"
    assert admin["role"] == "admin"


def test_invalid_token():
    """
    Test handling of an invalid JWT token.
    """
    invalid_token = "invalid.jwt.token"
    with pytest.raises(HTTPException) as exc_info:
        verify_jwt(invalid_token)
    assert exc_info.value.status_code == 401


def test_invalid_role():
    """
    Test handling of a token with an incorrect role.
    """
    data = {"sub": "testuser", "role": "user"}
    token = create_access_token(data)
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin(token)
    assert exc_info.value.status_code == 401


def test_expired_token():
    """
    Test handling of an expired token.
    """
    data = {"sub": "testuser", "role": "user"}
    with freeze_time(datetime.now(timezone.utc)) as frozen_time:
        token = create_access_token(data, expires_delta=timedelta(seconds=1))
        frozen_time.tick(delta=timedelta(seconds=2))
        with pytest.raises(HTTPException) as exc_info:
            verify_jwt(token)
        assert exc_info.value.status_code == 401
