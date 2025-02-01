"""
user_router.py

Defines user-related API routes, including registration, login, logout, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/login`: Authenticate a user and return a JWT token.
- `/logout`: Logout the currently authenticated user.
- `/profile`: Retrieve the profile of the currently authenticated user.

Features:
- Secure password handling and validation.
- Role-based access for user operations.
- Implements rate-limiting to prevent excessive API calls.
- Logs detailed user actions for security and audit purposes.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated
import redis

from janux_auth_gateway.config import Config
from janux_auth_gateway.schemas.user_schema import UserCreate, UserResponse
from janux_auth_gateway.schemas.response_schema import (
    ConflictResponse,
    UnauthorizedResponse,
)
from janux_auth_gateway.auth.passwords import hash_password
from janux_auth_gateway.auth.jwt import get_current_user
from janux_auth_gateway.models.user_model import User
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Constants
REDIS_HOST = Config.REDIS_HOST
REDIS_PORT = Config.REDIS_PORT

# Redis instance for rate-limiting user actions
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# User OAuth2 dependency
UserDependency = Annotated[dict, Depends(get_current_user)]

# Initialize router
user_router = APIRouter()


def is_rate_limited(user_email: str) -> bool:
    """
    Checks if a user is rate-limited to prevent excessive API requests.

    Args:
        user_email (str): The email of the user attempting an action.

    Returns:
        bool: True if the user is rate-limited, False otherwise.
    """
    attempts_key = f"user_rate_limit:{user_email}"
    attempts = redis_client.get(attempts_key)
    if attempts and int(attempts) >= 10:
        return True
    return False


def record_user_action(user_email: str):
    """
    Records a user action for rate-limiting.

    Args:
        user_email (str): The email of the user performing an action.
    """
    attempts_key = f"user_rate_limit:{user_email}"
    redis_client.incr(attempts_key)
    redis_client.expire(attempts_key, 900)  # Reset after 15 minutes


@user_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Email already registered", "model": ConflictResponse},
        401: {"description": "Unauthorized access", "model": UnauthorizedResponse},
    },
)
async def register_user(user: UserCreate):
    """
    Register a new user securely.
    """
    logger.info(f"Register endpoint accessed for email: {user.email}")

    if is_rate_limited(user.email):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )

    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
        )

    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email, full_name=user.full_name, hashed_password=hashed_password
    )
    await new_user.insert()
    record_user_action(user.email)

    return UserResponse(
        id=str(new_user.id), email=new_user.email, full_name=new_user.full_name
    )


@user_router.get(
    "/profile",
    responses={
        401: {"description": "Unauthorized access", "model": UnauthorizedResponse}
    },
)
async def get_profile(current_user: UserDependency):
    """
    Returns the profile of the currently logged-in user.
    """
    return {"message": "This is your profile", "user": current_user}


@user_router.post(
    "/logout",
    responses={
        401: {"description": "Unauthorized access", "model": UnauthorizedResponse}
    },
)
async def logout(current_user: UserDependency):
    """
    Logs out the currently authenticated user.
    """
    logger.info(f"Logout endpoint accessed for user: {current_user['username']}")
    return {"message": "You have been logged out successfully."}
