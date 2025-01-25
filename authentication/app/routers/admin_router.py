"""
admin_router.py

Defines admin-related API routes, including login, managing users, and retrieving admin profiles.

Endpoints:
- `/login`: Authenticate an admin and return a JWT token.
- `/users`: List all users (Admin only).
- `/users/{user_id}`: Delete a user by ID (Admin only).
- `/profile`: Retrieve the profile of the currently authenticated admin.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from typing import Annotated, List
from datetime import timedelta

from app.schemas.user import UserResponse
from app.auth.passwords import verify_password
from app.auth.jwt import create_access_token, get_current_admin
from app.models.admin import Admin
from app.models.user import User
from app.config import Config
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# Admin OAuth2 dependency
AdminDependency = Annotated[dict, Depends(get_current_admin)]

# Initialize router
admin_router = APIRouter()


@admin_router.post("/login")
async def login_admin(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Log in an admin by validating their credentials and generating a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials (username as email and password).

    Returns:
        dict: The access token and its type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    logger.info(f"Admin login endpoint accessed for email: {form_data.username}")

    # Extract credentials
    email = form_data.username  # OAuth2PasswordRequestForm uses 'username' for email
    password = form_data.password

    # Authenticate admin
    admin = await Admin.find_one(Admin.email == email)

    if not admin or not verify_password(password, admin.hashed_password):
        logger.warning(f"Login failed for admin email: {email}. Invalid credentials.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(f"Admin login successful for email: {email}")

    return {"access_token": access_token, "token_type": "bearer"}


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
