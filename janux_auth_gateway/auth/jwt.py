"""
jwt.py

This module handles JSON Web Token (JWT) creation, validation, user authentication, and token revocation.

Features:
- JWT access and refresh token generation with expiration.
- Token decoding and verification including revocation checks.
- Dependency-safe Redis client for blacklist token management.
- FastAPI-compatible user and admin extraction from tokens.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import jwt
import redis
from functools import lru_cache
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from starlette import status
from typing import Optional, Dict, Any

from janux_auth_gateway.config import Config
from hestia_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Constants
REFRESH_TOKEN_EXPIRE_DAYS = 7

# OAuth2 Bearer configuration
user_oauth2_bearer = OAuth2PasswordBearer(tokenUrl=Config.ADMIN_TOKEN_URL)
admin_oauth2_bearer = OAuth2PasswordBearer(tokenUrl=Config.USER_TOKEN_URL)


@lru_cache()
def get_redis_client() -> redis.Redis:
    """
    Creates and returns a cached Redis client instance for token blacklisting.

    This function is dependency-injection safe for FastAPI and avoids deepcopy issues
    with thread-locked objects like Redis connections.

    Returns:
        redis.Redis: An active Redis client instance.
    """
    return redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)


def _create_jwt(data: Dict[str, Any], expires_delta: timedelta, key: str) -> str:
    """
    Internal helper to create a JWT with expiry, issuer, audience, and issued-at timestamp.

    Args:
        data (Dict[str, Any]): Payload to encode into the JWT.
        expires_delta (timedelta): Token lifespan.
        key (str): Private key used to sign the token.

    Returns:
        str: Encoded JWT token.
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
    Creates a signed JWT access token for user or admin authentication.

    Args:
        data (Dict[str, Any]): Token payload (e.g. {"sub": email, "role": "user"}).
        expires_delta (Optional[timedelta]): Expiration window. Defaults to configured minutes.

    Returns:
        str: Signed access token as a JWT string.
    """
    expires = expires_delta or timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_jwt(data, expires, Config.JWT_PRIVATE_KEY)


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Creates a long-lived JWT refresh token.

    Adds a `"type": "refresh"` field to distinguish from access tokens.

    Args:
        data (Dict[str, Any]): Token payload.

    Returns:
        str: Signed refresh token as a JWT string.
    """
    data["type"] = "refresh"
    return _create_jwt(
        data, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), Config.JWT_PRIVATE_KEY
    )


def verify_jwt(token: str, redis_client: redis.Redis) -> Dict[str, Any]:
    """
    Verifies and decodes a JWT token, checking expiration, issuer, audience, and blacklist.

    Args:
        token (str): Encoded JWT token.
        redis_client (redis.Redis): Redis client for blacklist check.

    Returns:
        Dict[str, Any]: Decoded token payload.

    Raises:
        HTTPException: If token is revoked, expired, or invalid.
    """
    if redis_client.get(token.encode()):
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
    redis_client: redis.Redis = Depends(get_redis_client),
) -> Dict[str, Any]:
    """
    FastAPI dependency to extract and validate the currently logged-in user.

    Args:
        token (str): JWT access token.
        redis_client (redis.Redis): Redis client for blacklist check.

    Returns:
        Dict[str, Any]: Token payload containing username and role.

    Raises:
        HTTPException: If role is not 'user' or token is invalid.
    """
    payload = verify_jwt(token, redis_client=redis_client)

    if payload.get("role") != "user":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user"
        )

    return {"username": payload["sub"], "role": payload["role"]}


def get_current_admin(
    token: str = Depends(admin_oauth2_bearer),
    redis_client: redis.Redis = Depends(get_redis_client),
) -> Dict[str, Any]:
    """
    FastAPI dependency to extract and validate the currently logged-in admin.

    Args:
        token (str): JWT access token.
        redis_client (redis.Redis): Redis client for blacklist check.

    Returns:
        Dict[str, Any]: Token payload containing admin's username and role.

    Raises:
        HTTPException: If role is not 'admin' or token is invalid.
    """
    payload = verify_jwt(token, redis_client=redis_client)

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate admin"
        )

    return {"username": payload["sub"], "role": payload["role"]}


def revoke_token(
    token: str, redis_client: redis.Redis = Depends(get_redis_client)
) -> None:
    """
    Adds the token to the Redis blacklist, effectively revoking it until it expires.

    Args:
        token (str): JWT access token to revoke.
        redis_client (redis.Redis): Redis client instance.

    Returns:
        None
    """
    redis_client.set(
        token.encode(), "revoked", ex=Config.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    logger.info(f"Token revoked successfully: {token}")
