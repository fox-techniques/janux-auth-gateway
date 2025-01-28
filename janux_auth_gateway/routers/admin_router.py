"""
admin_router.py

Defines admin-related API routes, including login, managing users, retrieving admin profiles, and logging out.

Endpoints:
- `/login`: Authenticate an admin and return a JWT token.
- `/users`: List all users (Admin only).
- `/users/{user_id}`: Delete a user by ID (Admin only).
- `/profile`: Retrieve the profile of the currently authenticated admin.
- `/logout`: Logout the currently authenticated admin.

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
from janux_auth_gateway.debug.custom_logger import get_logger

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

    Raises:
        HTTPException: If any unexpected error occurs during the operation.
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
        HTTPException: If the user ID does not exist or if any unexpected error occurs.
    """
    try:
        logger.info(
            f"Admin deletion endpoint accessed by: {current_admin['username']} for user ID: {user_id}"
        )

        user = await User.get(user_id)
        if not user:
            logger.warning(f"User deletion failed: User ID {user_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )

        await user.delete()
        logger.info(f"User ID {user_id} successfully deleted.")

        return {"message": f"User ID {user_id} successfully deleted."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user. Please try again later.",
        )


@admin_router.get("/profile")
async def get_profile(current_admin: AdminDependency):
    """
    Protected route: Returns the profile of the currently logged-in admin.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        dict: The admin's profile information.

    Raises:
        HTTPException: If any unexpected error occurs during the operation.
    """
    try:
        logger.info(f"Profile endpoint accessed for admin: {current_admin['username']}")

        return {
            "message": "This is your admin profile",
            "admin": current_admin,
        }
    except KeyError as e:
        logger.error(f"Error accessing admin profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving admin profile. Please try again later.",
        )


@admin_router.post("/logout")
async def logout(current_admin: AdminDependency):
    """
    Logs out the currently authenticated admin by invalidating their token.

    Args:
        current_admin (dict): The currently authenticated admin user.

    Returns:
        dict: A confirmation message.

    Raises:
        HTTPException: If any unexpected error occurs during the operation.
    """
    try:
        logger.info(f"Logout endpoint accessed for admin: {current_admin['username']}")

        # Placeholder logic for logout (e.g., blacklist token, clear session)
        return {"message": "You have been logged out successfully."}
    except KeyError as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error logging out. Please try again later.",
        )
