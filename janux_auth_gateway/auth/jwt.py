"""
jwt.py

This module handles JSON Web Token (JWT) creation, validation, and user authentication.

Features:
- Token creation with expiration and optional unique identifiers (jti).
- Validation and decoding of tokens to retrieve current user information.
- Environment variable integration for private and public keys.
- Implements refresh tokens for automatic re-authentication.
- Supports token revocation (blacklisting) for secure logout.

Replaced python-jose with PyJWT for enhanced security.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import jwt
import redis
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from starlette import status
from typing import Optional, Dict, Any

from janux_auth_gateway.config import Config
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Constants
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Redis instance for token blacklisting
blacklist = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

# OAuth2 Bearer configuration
user_oauth2_bearer = OAuth2PasswordBearer(tokenUrl=Config.ADMIN_TOKEN_URL)
admin_oauth2_bearer = OAuth2PasswordBearer(tokenUrl=Config.USER_TOKEN_URL)


def _create_jwt(data: Dict[str, Any], expires_delta: timedelta, key: str) -> str:
    """
    Helper function to create a JWT token.

    Args:
        data (Dict[str, Any]): The payload data for the token.
        expires_delta (timedelta): The duration for which the token remains valid.
        key (str): The private key used to sign the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update(
        {
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "iss": Config.ISSUER,
            "aud": Config.AUDIENCE,
        }
    )
    return jwt.encode(to_encode, key, algorithm="RS256")


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token with optional expiration.

    Args:
        data (Dict[str, Any]): The payload data to include in the token.
        expires_delta (Optional[timedelta]): The token expiration period.

    Returns:
        str: A signed JWT access token.
    """
    expires = expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_jwt(data, expires, Config.JWT_PRIVATE_KEY)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Creates a long-lived refresh token for session continuity.

    Args:
        data (Dict[str, Any]): The payload data to include in the token.

    Returns:
        str: A signed JWT refresh token.
    """
    data["type"] = "refresh"
    return _create_jwt(
        data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), Config.JWT_PRIVATE_KEY
    )


def verify_jwt(token: str, redis_client=blacklist) -> Dict[str, Any]:
    """
    Verifies a JWT token, ensuring issuer and audience match, and checks if the token is revoked.

    Args:
        token (str): The JWT token to be verified.
        redis_client (redis.Redis): Redis instance (default is the real Redis server).

    Returns:
        Dict[str, Any]: The decoded JWT payload if valid.

    Raises:
        HTTPException: If the token is expired, invalid, or revoked.
    """
    if redis_client.get(token.encode()):  # Check if token is blacklisted
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked."
        )

    try:
        return jwt.decode(
            token,
            Config.JWT_PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=Config.ISSUER,
            audience=Config.AUDIENCE,
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )


def get_current_user(
    token: str = Depends(user_oauth2_bearer),
    redis_client=blacklist,
) -> Dict[str, Any]:
    """
    Retrieves the current user's details from the JWT token.

    Args:
        token (str): The JWT token provided by the user.
        redis_client (redis.Redis): Redis instance. Defaults to the real Redis server

    Returns:
        Dict[str, Any]: The decoded user information.

    Raises:
        HTTPException: If the user role is invalid.
    """
    payload = verify_jwt(token, redis_client=redis_client)

    if payload.get("role") != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    return {"username": payload["sub"], "role": payload["role"]}


def get_current_admin(
    token: str = Depends(admin_oauth2_bearer),
    redis_client=blacklist,
) -> Dict[str, Any]:
    """
    Retrieves the current admin's details from the JWT token.

    Args:
        token (str): The JWT token provided by the admin.
        redis_client (redis.Redis): Redis instance. Defaults to the real Redis server

    Returns:
        Dict[str, Any]: The decoded admin information.

    Raises:
        HTTPException: If the admin role is invalid.
    """
    payload = verify_jwt(token, redis_client=redis_client)

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin"
        )

    return {"username": payload["sub"], "role": payload["role"]}


def revoke_token(token: str, redis_client=blacklist):
    """
    Revokes a given token by adding it to the blacklist.

    Args:
        token (str): The JWT token to be revoked.
        redis_client (redis.Redis): Redis instance (default is the real Redis server).

    Returns:
        None
    """
    redis_client.set(
        token.encode(), "revoked", ex=Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    logger.info(f"Token revoked successfully: {token}")
