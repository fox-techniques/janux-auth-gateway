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

from app.config import Config
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")


# Constants
SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Config.ACCESS_TOKEN_EXPIRE_MINUTES

# OAuth2 Bearer configuration
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token with optional expiration time.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta, optional): The token expiration period. Defaults to None.

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


def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    """
    Decodes and validates the JWT token to retrieve the current user's information.

    Args:
        token (str): The JWT token provided by the client.

    Returns:
        dict: The decoded user information (e.g., username, ID).

    Raises:
        HTTPException: If the token is invalid or user data is missing.
    """
    logger.info("Getting current user...")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "id": user_id}
    except JWTError as e:
        logger.error(f"JWT decoding error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
