"""
jwt.py

This module handles JSON Web Token (JWT) creation, validation, and user authentication.

Features:
- Token creation with expiration and optional unique identifiers (jti).
- Validation and decoding of tokens to retrieve current user information.
- Environment variable integration for secret keys and algorithms.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from jose import jwt, JWTError
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
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 Bearer configuration
user_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
admin_oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a JWT access token with optional expiration time.

    Args:
        data (Dict[str, Any]): The payload data to include in the token.
        expires_delta (Optional[timedelta]): The token expiration period. Defaults to None.

    Returns:
        str: The encoded JWT token.
    """
    logger.info("Creating access token...")

    to_encode = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )

    to_encode.update(
        {"exp": expires, "jti": f"token-{datetime.now(timezone.utc).timestamp()}"}
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(user_oauth2_bearer)) -> Dict[str, Any]:
    """
    Decodes and validates the JWT token to retrieve the current user's information.

    Args:
        token (str): The JWT token provided by the client.

    Returns:
        Dict[str, Any]: The decoded user information (e.g., username, ID).

    Raises:
        HTTPException: If the token is invalid or user data is missing.
    """
    logger.info("Getting current user...")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or role != "user":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add validation for token payload to enhance security
        if not isinstance(username, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username, "role": role}

    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_admin(token: str = Depends(admin_oauth2_bearer)) -> Dict[str, Any]:
    """
    Decodes and validates the JWT token to retrieve the current admin's information.

    Args:
        token (str): The JWT token provided by the client.

    Returns:
        Dict[str, Any]: The decoded admin information (e.g., username, ID).

    Raises:
        HTTPException: If the token is invalid or admin data is missing.
    """
    logger.info("Getting current admin...")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")

        if not username or role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate admin",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Add validation for token payload to enhance security
        if not isinstance(username, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"username": username, "role": role}

    except JWTError as e:
        logger.error(f"JWT decoding error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
