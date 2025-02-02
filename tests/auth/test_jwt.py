"""
test_jwt.py

Unit tests for the JWT authentication module in the JANUX Authentication Gateway.

Tests:
- Token creation (access & refresh tokens).
- Token verification, expiration, and invalidation.
- User & admin authentication using JWTs.
- Token revocation (blacklisting).

Features:
- Uses `fakeredis` for an in-memory Redis instance.
- Mocks `Config.PRIVATE_KEY`, `Config.PUBLIC_KEY` for RSA signing.
- Ensures only valid JWTs are accepted, and revoked tokens are rejected.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import jwt
import fakeredis
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from fastapi import HTTPException
from janux_auth_gateway.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_jwt,
    get_current_user,
    get_current_admin,
    revoke_token,
)
from janux_auth_gateway.config import Config


@pytest.fixture()
def mock_keys(mocker):
    """
    Mock JWT private and public keys as valid RSA keys.
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_pem = (
        private_key.public_key()
        .public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        .decode("utf-8")
    )

    # Mock Config values with valid RSA keys
    mocker.patch.object(Config, "PRIVATE_KEY", private_pem)
    mocker.patch.object(Config, "PUBLIC_KEY", public_pem)


@pytest.fixture()
def fake_redis():
    """
    Creates an in-memory Redis instance for testing.
    """
    return fakeredis.FakeRedis(decode_responses=True)


def test_create_access_token(mock_keys):
    """
    Test that an access token is created successfully.

    Expected Outcome:
    - Returns a valid JWT string.
    """
    token = create_access_token({"sub": "testuser", "role": "user"})
    assert isinstance(token, str)


def test_create_refresh_token(mock_keys):
    """
    Test that a refresh token is created successfully.

    Expected Outcome:
    - Returns a valid JWT string.
    """
    token = create_refresh_token({"sub": "testuser"})
    assert isinstance(token, str)


def test_verify_valid_jwt(mock_keys, fake_redis):
    """
    Test that a valid JWT is verified successfully.

    Expected Outcome:
    - Decoded payload should contain expected claims.
    """
    token = create_access_token({"sub": "testuser", "role": "user"})

    decoded = verify_jwt(token, redis_client=fake_redis)

    assert decoded["sub"] == "testuser"
    assert decoded["role"] == "user"


def test_verify_revoked_jwt(mock_keys, fake_redis):
    """
    Test that a revoked JWT raises an exception.

    Expected Outcome:
    - Should return a 401 Unauthorized error.
    """
    token = create_access_token({"sub": "testuser"})

    fake_redis.set(token.encode(), "revoked")

    with pytest.raises(HTTPException, match="Token revoked."):
        verify_jwt(token, redis_client=fake_redis)


def test_verify_expired_jwt(mock_keys, fake_redis):
    """
    Test that an expired JWT raises an exception.

    Expected Outcome:
    - Should return a 401 Unauthorized error.
    """
    expired_token = jwt.encode(
        {"sub": "testuser", "exp": 0},
        Config.PRIVATE_KEY,
        algorithm="RS256",
    )

    with pytest.raises(HTTPException, match="Token has expired."):
        verify_jwt(expired_token, redis_client=fake_redis)


def test_revoke_token(mock_keys, fake_redis):
    """
    Test that a token is successfully revoked.

    Expected Outcome:
    - Token should be stored in Redis with `revoked` status.
    """
    token = create_access_token({"sub": "testuser"})

    revoke_token(token, redis_client=fake_redis)

    assert fake_redis.get(token.encode()) == "revoked"


def test_get_current_user_valid(mock_keys, fake_redis):
    """
    Test that a valid user token returns user details.

    Expected Outcome:
    - Returns a dictionary with `username` and `role`.
    """
    token = create_access_token({"sub": "test@example.com", "role": "user"})

    user_data = get_current_user(token, redis_client=fake_redis)

    assert user_data["username"] == "test@example.com"
    assert user_data["role"] == "user"


def test_get_current_user_invalid_role(mock_keys, fake_redis):
    """
    Test that a token with an invalid role raises an exception.

    Expected Outcome:
    - Should return a 401 Unauthorized error.
    """
    token = create_access_token({"sub": "test@example.com", "role": "admin"})

    with pytest.raises(HTTPException, match="Could not validate user"):
        get_current_user(token, redis_client=fake_redis)


def test_get_current_admin_valid(mock_keys, fake_redis):
    """
    Test that a valid admin token returns admin details.

    Expected Outcome:
    - Returns a dictionary with `username` and `role`.
    """
    token = create_access_token({"sub": "admin@example.com", "role": "admin"})

    admin_data = get_current_admin(token, redis_client=fake_redis)

    assert admin_data["username"] == "admin@example.com"
    assert admin_data["role"] == "admin"


def test_get_current_admin_invalid_role(mock_keys, fake_redis):
    """
    Test that a token with an invalid admin role raises an exception.

    Expected Outcome:
    - Should return a 401 Unauthorized error.
    """
    token = create_access_token({"sub": "test@example.com", "role": "user"})

    with pytest.raises(HTTPException, match="Could not validate admin"):
        get_current_admin(token, redis_client=fake_redis)
