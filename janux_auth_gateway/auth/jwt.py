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

# Redis instance for token blacklisting
blacklist = redis.Redis(host="localhost", port=6379, db=0)

# Constants
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth2 Bearer configuration
user_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
admin_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


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
            "iss": "your-auth-server.com",
            "aud": "your-client-app",
        }
    )
    return jwt.encode(to_encode, key, algorithm="RS256")


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Creates a short-lived access token for user authentication.

    Args:
        data (Dict[str, Any]): The payload data to include in the token.

    Returns:
        str: A signed JWT access token.
    """
    return _create_jwt(
        data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), Config.PRIVATE_KEY
    )


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
        data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), Config.PRIVATE_KEY
    )


def verify_jwt(token: str) -> Dict[str, Any]:
    """
    Verifies a JWT token, ensuring issuer and audience match, and checks if the token is revoked.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        Dict[str, Any]: The decoded JWT payload if valid.

    Raises:
        HTTPException: If the token is expired, invalid, or revoked.
    """
    if blacklist.get(token):  # Check if token is blacklisted
        raise HTTPException(status_code=401, detail="Token revoked.")

    try:
        return jwt.decode(
            token,
            Config.PUBLIC_KEY,
            algorithms=["RS256"],
            issuer="your-auth-server.com",
            audience="your-client-app",
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired."
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )


def get_current_user(token: str = Depends(user_oauth2_bearer)) -> Dict[str, Any]:
    """
    Retrieves the current user's details from the JWT token.

    Args:
        token (str): The JWT token provided by the user.

    Returns:
        Dict[str, Any]: The decoded user information.

    Raises:
        HTTPException: If the user role is invalid.
    """
    logger.info("Getting current user...")
    payload = verify_jwt(token)
    if payload.get("role") != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )
    return {"username": payload["sub"], "role": payload["role"]}


def get_current_admin(token: str = Depends(admin_oauth2_bearer)) -> Dict[str, Any]:
    """
    Retrieves the current admin's details from the JWT token.

    Args:
        token (str): The JWT token provided by the admin.

    Returns:
        Dict[str, Any]: The decoded admin information.

    Raises:
        HTTPException: If the admin role is invalid.
    """
    logger.info("Getting current admin...")
    payload = verify_jwt(token)
    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin"
        )
    return {"username": payload["sub"], "role": payload["role"]}


def revoke_token(token: str):
    """
    Revokes a given token by adding it to the blacklist.

    Args:
        token (str): The JWT token to be revoked.

    Returns:
        None
    """
    blacklist.set(token, "revoked", ex=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    logger.info("Token revoked successfully.")
