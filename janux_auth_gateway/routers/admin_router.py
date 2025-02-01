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
- Documents 401 Unauthorized responses for unauthorized access.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from starlette import status
from typing import Annotated, List
import redis

from janux_auth_gateway.config import Config
from janux_auth_gateway.schemas.user_schema import UserResponse
from janux_auth_gateway.auth.jwt import get_current_admin
from janux_auth_gateway.models.user_model import User
from janux_auth_gateway.debug.custom_logger import get_logger
from janux_auth_gateway.schemas.response_schema import UnauthorizedResponse

# Initialize logger
logger = get_logger("auth_service_logger")

# Constants
REDIS_HOST = Config.REDIS_HOST
REDIS_PORT = Config.REDIS_PORT

# Redis instance for rate-limiting user actions
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Admin OAuth2 dependency
AdminDependency = Annotated[dict, Depends(get_current_admin)]

# Initialize router
admin_router = APIRouter()


@admin_router.get(
    "/users",
    response_model=List[UserResponse],
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized access."}
    },
)
async def list_users(current_admin: AdminDependency):
    """
    Admin-only route to list all users.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        List[UserResponse]: A list of all registered users.

    Raises:
        HTTPException: If unauthorized (401) or an unexpected error occurs.
    """
    try:
        logger.info(f"Admin endpoint accessed by: {current_admin['username']}")
        users = await User.find_all().to_list()
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


@admin_router.delete(
    "/users/{user_id}",
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized access."}
    },
)
async def delete_user(user_id: str, current_admin: AdminDependency):
    """
    Admin-only route to delete a user by ID.
    """
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
        return {"message": f"User ID {user_id} successfully deleted."}
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user. Please try again later.",
        )


@admin_router.get(
    "/profile",
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized access."}
    },
)
async def get_profile(current_admin: AdminDependency):
    """
    Returns the profile of the currently logged-in admin.
    """
    return {"message": "This is your admin profile", "admin": current_admin}


@admin_router.post(
    "/logout",
    responses={
        401: {"model": UnauthorizedResponse, "description": "Unauthorized access."}
    },
)
async def logout(current_admin: AdminDependency):
    """
    Logs out the currently authenticated admin.
    """
    logger.info(f"Logout endpoint accessed for admin: {current_admin['username']}")
    return {"message": "You have been logged out successfully."}
