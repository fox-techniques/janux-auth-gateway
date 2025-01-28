"""
auth_router.py

Defines authentication-related API routes for the JANUX Authentication Gateway.

Endpoints:
- `/login`: Unified login endpoint for both users and admins.

Features:
- Validates user and admin credentials securely.
- Issues JWT tokens with appropriate roles and expiration.
- Detailed logging for authentication operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from starlette import status
from janux_auth_gateway.auth.jwt import create_access_token
from janux_auth_gateway.database.mongoDB import authenticate_user, authenticate_admin
from janux_auth_gateway.config import Config
from janux_auth_gateway.schemas.token import Token
from janux_auth_gateway.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Initialize router
auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Unified login endpoint for both users and admins.

    Args:
        form_data (OAuth2PasswordRequestForm): Login form containing username and password.

    Returns:
        Token: A JWT token with the authenticated user's role and expiration.

    Raises:
        HTTPException: If authentication fails.
    """
    email = form_data.username
    password = form_data.password

    logger.info(f"Login attempt for email: {email}")

    if await authenticate_admin(email, password):
        role = "admin"
    elif await authenticate_user(email, password):
        role = "user"
    else:
        logger.warning(f"Authentication failed for email: {email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": email, "role": role},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(f"Login successful for email: {email}, role: {role}")
    return Token(access_token=access_token, token_type="bearer")
