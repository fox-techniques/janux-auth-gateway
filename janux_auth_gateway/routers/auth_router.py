"""
auth_router.py

Defines authentication-related API routes for the JANUX Authentication Gateway.

Endpoints:
- `/login`: Unified login endpoint for both users and admins.

Features:
- Validates user and admin credentials securely.
- Issues JWT tokens with appropriate roles and expiration.
- Detailed logging for authentication operations.
- Prevents brute-force attacks with rate limiting.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from starlette import status
import redis

from janux_auth_gateway.auth.jwt import create_access_token
from janux_auth_gateway.database.mongoDB import authenticate_user, authenticate_admin
from janux_auth_gateway.config import Config
from janux_auth_gateway.schemas.token_schema import Token
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Redis instance for rate-limiting login attempts
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Initialize router
auth_router = APIRouter()


def is_rate_limited(email: str) -> bool:
    """
    Checks if a login attempt is rate-limited to prevent brute-force attacks.

    Args:
        email (str): The email of the user attempting to log in.

    Returns:
        bool: True if the login attempt is blocked due to too many failed attempts.
    """
    attempts_key = f"login_attempts:{email}"
    attempts = redis_client.get(attempts_key)
    if attempts and int(attempts) >= 5:
        return True
    return False


def record_failed_attempt(email: str):
    """
    Records a failed login attempt for rate limiting.

    Args:
        email (str): The email of the user who failed authentication.
    """
    attempts_key = f"login_attempts:{email}"
    redis_client.incr(attempts_key)
    redis_client.expire(
        attempts_key, 900
    )  # Block for 15 minutes after 5 failed attempts


def reset_failed_attempts(email: str):
    """
    Resets failed login attempts on a successful authentication.

    Args:
        email (str): The email of the user who successfully authenticated.
    """
    attempts_key = f"login_attempts:{email}"
    redis_client.delete(attempts_key)


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Unified login endpoint for both users and admins.

    Args:
        form_data (OAuth2PasswordRequestForm): Login form containing username and password.

    Returns:
        Token: A JWT token with the authenticated user's role and expiration.

    Raises:
        HTTPException: If authentication fails or rate limit is exceeded.
    """
    email = form_data.username
    password = form_data.password

    logger.info(f"Login attempt for email: {email}")

    if is_rate_limited(email):
        logger.warning(
            f"Login blocked for email: {email} due to too many failed attempts."
        )
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    if await authenticate_admin(email, password):
        role = "admin"
    elif await authenticate_user(email, password):
        role = "user"
    else:
        logger.warning(f"Authentication failed for email: {email}")
        record_failed_attempt(email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    reset_failed_attempts(email)
    access_token = create_access_token(
        data={"sub": email, "role": role},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(f"Login successful for email: {email}, role: {role}")
    return Token(access_token=access_token, token_type="bearer")
