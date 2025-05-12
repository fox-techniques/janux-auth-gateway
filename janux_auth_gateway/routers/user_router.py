"""
user_router.py

Defines user-related API routes, including registration, login, logout, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/logout`: Logout the currently authenticated user.
- `/profile`: Retrieve the profile of the currently authenticated user.

Features:
- Secure password handling and validation.
- Role-based access for user operations.
- Implements rate-limiting to prevent excessive API calls.
- Logs detailed user actions for security and audit purposes.
- Supports both MongoDB and PostgreSQL backends dynamically.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated
import redis

from janux_auth_gateway.config import Config
from janux_auth_gateway.schemas.response_schema import (
    ConflictResponse,
    UnauthorizedResponse,
)
from janux_auth_gateway.auth.passwords import hash_password
from janux_auth_gateway.auth.jwt import get_current_user
from hestia_logger import get_logger

# Import backend-specific schemas and models
if Config.AUTH_DB_BACKEND == "mongo":
    from janux_auth_gateway.schemas.user_schema_mongo import (
        UserResponseMongo as UserResponse,
        UserCreateMongo as UserCreate,
    )
    from janux_auth_gateway.models.mongoDB.user_model import User
elif Config.AUTH_DB_BACKEND == "postgres":
    from janux_auth_gateway.schemas.user_schema_postgres import (
        UserResponsePostgres as UserResponse,
        UserCreatePostgres as UserCreate,
    )
    from janux_auth_gateway.models.postgreSQL.user_model import User

# Logger instance
logger = get_logger("auth_service_logger")

# Redis client for rate-limiting
redis_client = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

# FastAPI dependency for authenticated user
UserDependency = Annotated[dict, Depends(get_current_user)]

# Initialize the router
user_router = APIRouter()


def is_rate_limited(identifier: str) -> bool:
    """
    Checks if a user is rate-limited to prevent excessive API requests.

    Args:
        identifier (str): The unique user identifier (email or username).

    Returns:
        bool: True if the user is rate-limited, False otherwise.
    """
    attempts_key = f"user_rate_limit:{identifier}"
    attempts = redis_client.get(attempts_key)
    return bool(attempts and int(attempts) >= 10)


def record_user_action(identifier: str):
    """
    Records a user action for rate-limiting purposes.

    Args:
        identifier (str): The unique user identifier (email or username).
    """
    attempts_key = f"user_rate_limit:{identifier}"
    redis_client.incr(attempts_key)
    redis_client.expire(attempts_key, 900)  # 15-minute cooldown


@user_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "User already registered", "model": ConflictResponse},
        401: {"description": "Unauthorized access", "model": UnauthorizedResponse},
    },
)
async def register_user(user: UserCreate):
    """
    Register a new user securely.

    Args:
        user (UserCreate): User registration details.

    Returns:
        UserResponse: The registered user's public information.

    Raises:
        HTTPException: If the user already exists or is rate-limited.
    """
    identifier = user.email if Config.AUTH_DB_BACKEND == "mongo" else user.username
    logger.info(f"Register endpoint accessed for user: {identifier}")

    if is_rate_limited(identifier):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )

    if Config.AUTH_DB_BACKEND == "mongo":
        existing_user = await User.find_one(User.email == user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered."
            )
        hashed_password = hash_password(user.password)
        new_user = User(
            email=user.email,
            full_name=user.full_name,
            hashed_password=hashed_password,
        )
        await new_user.insert()
    else:
        from sqlalchemy.future import select
        from janux_auth_gateway.database.postgreSQL import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.username == user.username)
            )
            existing_user = result.scalar_one_or_none()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already registered.",
                )
            hashed_password = hash_password(user.password)
            new_user = User(
                username=user.username,
                full_name=user.full_name,
                hashed_password=hashed_password,
            )
            session.add(new_user)
            await session.commit()

    record_user_action(identifier)

    if Config.AUTH_DB_BACKEND == "mongo":
        return UserResponse(
            id=str(new_user.id),
            email=new_user.email,
            full_name=new_user.full_name,
        )
    else:
        return UserResponse(
            id=str(new_user.id),
            username=new_user.username,
            full_name=new_user.full_name,
        )


@user_router.get(
    "/profile",
    responses={
        401: {"description": "Unauthorized access", "model": UnauthorizedResponse}
    },
)
async def get_profile(current_user: UserDependency):
    """
    Returns the profile of the currently authenticated user.

    Args:
        current_user (dict): Authenticated user context from JWT.

    Returns:
        dict: A message and the user's profile data.
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

    Args:
        current_user (dict): Authenticated user context from JWT.

    Returns:
        dict: A message confirming successful logout.
    """
    logger.info(f"Logout endpoint accessed for user: {current_user['username']}")
    return {"message": "You have been logged out successfully."}
