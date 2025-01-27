"""
user_router.py

Defines user-related API routes, including registration, login, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/login`: Authenticate a user and return a JWT token.
- `/profile`: Retrieve the profile of the currently authenticated user.

Features:
- Secure password handling and validation.
- Role-based access for user operations.
- Detailed logging for all operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated

from app.schemas.user import UserCreate, UserResponse
from app.schemas.response import ConflictResponse
from app.auth.passwords import hash_password
from app.auth.jwt import get_current_user
from app.models.user import User
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# User OAuth2 dependency
UserDependency = Annotated[dict, Depends(get_current_user)]

# Initialize router
user_router = APIRouter()


@user_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "Email already registered", "model": ConflictResponse}
    },
)
async def register_user(user: UserCreate):
    """
    Register a new user using Beanie for database operations.

    Args:
        user (UserCreate): The user data for registration.

    Returns:
        UserResponse: The created user's response data.

    Raises:
        HTTPException: If the email is already registered.
    """
    logger.info(f"Register endpoint accessed for email: {user.email}")

    # Check if the user already exists
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        logger.warning(
            f"User registration failed. Email {user.email} is already registered."
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    # Create and insert the user
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    await new_user.insert()

    logger.info(f"User {user.email} registered successfully.")
    return UserResponse(
        id=str(new_user.id), email=new_user.email, full_name=new_user.full_name
    )


@user_router.get("/profile")
async def get_profile(current_user: UserDependency):
    """
    Protected route: Returns the profile of the currently logged-in user.

    Args:
        current_user (dict): The currently authenticated user (injected by `get_current_user`).

    Returns:
        dict: The user's profile information.
    """
    logger.info(f"Profile endpoint accessed for user: {current_user['username']}")

    return {
        "message": "This is your profile",
        "user": current_user,
    }
