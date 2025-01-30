"""
admin_router.py

Defines admin-related API routes, including login, managing users, retrieving admin profiles, and logging out.

Endpoints:
- `/users`: List all users (Admin only).
- `/users/{user_id}`: Delete a user by ID (Admin only).
- `/profile`: Retrieve the profile of the currently authenticated admin.
- `/logout`: Logout the currently authenticated admin.

Features:
- Role-based access for admin operations.
- Secure password handling and validation.
- Implements rate-limiting to prevent excessive API calls.
- Logs detailed admin actions for audit and security.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated, List
import redis

from janux_auth_gateway.schemas.user import UserResponse
from janux_auth_gateway.auth.jwt import get_current_admin
from janux_auth_gateway.models.user import User
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Redis instance for rate-limiting admin actions
redis_client = redis.Redis(host="localhost", port=6379, db=0)

# Admin OAuth2 dependency
AdminDependency = Annotated[dict, Depends(get_current_admin)]

# Initialize router
admin_router = APIRouter()


def is_rate_limited(admin_id: str) -> bool:
    """
    Checks if an admin is rate-limited to prevent excessive API usage.

    Args:
        admin_id (str): The ID of the admin user.

    Returns:
        bool: True if the admin is rate-limited, False otherwise.
    """
    attempts_key = f"admin_rate_limit:{admin_id}"
    attempts = redis_client.get(attempts_key)
    if attempts and int(attempts) >= 10:
        return True
    return False


def record_admin_action(admin_id: str):
    """
    Records an admin action for rate-limiting.

    Args:
        admin_id (str): The ID of the admin user.
    """
    attempts_key = f"admin_rate_limit:{admin_id}"
    redis_client.incr(attempts_key)
    redis_client.expire(attempts_key, 900)  # 15-minute reset window


@admin_router.get("/users", response_model=List[UserResponse])
async def list_users(current_admin: AdminDependency):
    """
    Admin-only route to list all users.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        List[UserResponse]: A list of all registered users.

    Raises:
        HTTPException: If any unexpected error occurs during the operation or rate-limit is exceeded.
    """
    if is_rate_limited(current_admin["username"]):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )

    try:
        logger.info(f"Admin endpoint accessed by: {current_admin['username']}")
        users = await User.find_all().to_list()
        record_admin_action(current_admin["username"])
        return [
            UserResponse(id=str(user.id), email=user.email, full_name=user.full_name)
            for user in users
        ]
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error listing users. Please try again later.",
        )


@admin_router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_admin: AdminDependency):
    """
    Admin-only route to delete a user by ID.
    """
    if is_rate_limited(current_admin["username"]):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Please try again later.",
        )

    try:
        logger.info(
            f"Admin deletion endpoint accessed by: {current_admin['username']} for user ID: {user_id}"
        )
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        await user.delete()
        record_admin_action(current_admin["username"])
        return {"message": f"User ID {user_id} successfully deleted."}
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user. Please try again later.",
        )


@admin_router.get("/profile")
async def get_profile(current_admin: AdminDependency):
    """
    Returns the profile of the currently logged-in admin.
    """
    return {"message": "This is your admin profile", "admin": current_admin}


@admin_router.post("/logout")
async def logout(current_admin: AdminDependency):
    """
    Logs out the currently authenticated admin.
    """
    logger.info(f"Logout endpoint accessed for admin: {current_admin['username']}")
    return {"message": "You have been logged out successfully."}
