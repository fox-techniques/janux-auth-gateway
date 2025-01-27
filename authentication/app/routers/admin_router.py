"""
admin_router.py

Defines admin-related API routes, including login, managing users, and retrieving admin profiles.

Endpoints:
- `/login`: Authenticate an admin and return a JWT token.
- `/users`: List all users (Admin only).
- `/users/{user_id}`: Delete a user by ID (Admin only).
- `/profile`: Retrieve the profile of the currently authenticated admin.

Features:
- Role-based access for admin operations.
- Secure password handling and validation.
- Detailed logging for all admin operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated, List

from app.schemas.user import UserResponse
from app.auth.jwt import get_current_admin
from app.models.user import User
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# Admin OAuth2 dependency
AdminDependency = Annotated[dict, Depends(get_current_admin)]

# Initialize router
admin_router = APIRouter()


@admin_router.get("/users", response_model=List[UserResponse])
async def list_users(current_admin: AdminDependency):
    """
    Admin-only route to list all users.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        List[UserResponse]: A list of all registered users.
    """
    logger.info(f"Admin endpoint accessed by: {current_admin['username']}")

    users = await User.find_all().to_list()
    return [
        UserResponse(id=str(user.id), email=user.email, full_name=user.full_name)
        for user in users
    ]


@admin_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_admin: AdminDependency):
    """
    Admin-only route to delete a user by ID.

    Args:
        user_id (str): The ID of the user to delete.
        current_admin (dict): The currently authenticated admin user.

    Returns:
        dict: A confirmation message.

    Raises:
        HTTPException: If the user ID does not exist.
    """
    logger.info(
        f"Admin deletion endpoint accessed by: {current_admin['username']} for user ID: {user_id}"
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


@admin_router.get("/profile")
async def get_profile(current_admin: AdminDependency):
    """
    Protected route: Returns the profile of the currently logged-in admin.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        dict: The admin's profile information.
    """
    logger.info(f"Profile endpoint accessed for admin: {current_admin['username']}")

    return {
        "message": "This is your admin profile",
        "admin": current_admin,
    }
