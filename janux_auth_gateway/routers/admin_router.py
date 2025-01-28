"""
admin_router.py

Defines admin-related API routes, including login, managing users, and retrieving admin profiles.

Endpoints:
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
from janux_auth_gateway.schemas.user import UserResponse
from janux_auth_gateway.auth.jwt import get_current_admin
from janux_auth_gateway.models.user import User
from janux_auth_gateway.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

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
