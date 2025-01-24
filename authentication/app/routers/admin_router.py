"""
admin_router.py

Defines admin-related API routes, including registration, login, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/login`: Authenticate a user and return a JWT token.
- `/logout`: Log out the currently authenticated user.
- `/profile`: Retrieve the profile of the currently authenticated user.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.response import ConflictResponse
from app.auth.passwords import hash_password, verify_password
from app.auth.jwt import create_access_token, get_current_user
from app.models.user import User
from app.config import Config
from app.logging.custom_logger import get_logger

from typing import List

# Initialize logger
logger = get_logger("app_logger")

# Initialize router
admin_router = APIRouter()

# In-memory token blacklist (replace with a persistent store in production)
TOKEN_BLACKLIST = set()


# Role-based access control decorator
def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )


@admin_router.get("/users", response_model=List[UserResponse])
async def list_users(current_user: dict = Depends(admin_required)):
    """
    Admin-only route to list all users.

    Args:
        current_user (dict): The currently authenticated admin user.

    Returns:
        List[UserResponse]: A list of all registered users.
    """
    logger.info(f"Admin endpoint accessed by: {current_user['username']}")

    users = await User.find_all().to_list()
    return [
        UserResponse(id=str(user.id), email=user.email, full_name=user.full_name)
        for user in users
    ]


@admin_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(admin_required)):
    """
    Admin-only route to delete a user by ID.

    Args:
        user_id (str): The ID of the user to delete.
        current_user (dict): The currently authenticated admin user.

    Returns:
        dict: A confirmation message.
    """
    logger.info(
        f"Admin deletion endpoint accessed by: {current_user['username']} for user ID: {user_id}"
    )

    user = await User.get(user_id)
    if not user:
        logger.warning(f"User deletion failed: User ID {user_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    await user.delete()
    logger.info(f"User ID {user_id} successfully deleted.")

    return {"message": f"User ID {user_id} successfully deleted."}
