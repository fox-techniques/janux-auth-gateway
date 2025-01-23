"""
user_router.py

Defines user-related API routes, including registration, login, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/login`: Authenticate a user and return a JWT token.
- `/profile`: Retrieve the profile of the currently authenticated user.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from datetime import timedelta

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.response import ConflictResponse
from app.auth.passwords import hash_password
from app.database.mongoDB import authenticate_user, username_exists, users_collection
from app.auth.jwt import create_access_token, get_current_user
from app.config import Config
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

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
    Register a new user. Hash the password and store user details in MongoDB.

    Args:
        user (UserCreate): The user registration data.

    Returns:
        UserResponse: The registered user's details.

    Raises:
        HTTPException: If the email is already registered.
    """
    logger.info(f"Register endpoint accessed for email: {user.email}")

    # Check if user already exists
    existing_user = username_exists(user.email)
    if existing_user:
        logger.warning(f"Registration failed: Email {user.email} already registered.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Insert the user into the database
    user_data = {
        "email": user.email,
        "full_name": user.full_name,
        "password": hashed_password,
    }
    result = users_collection.insert_one(user_data)

    logger.info(f"User registered successfully with email: {user.email}")

    # Return the created user
    return UserResponse(
        id=str(result.inserted_id), email=user.email, full_name=user.full_name
    )


@user_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user by validating their credentials and generating a JWT token.

    Args:
        form_data (OAuth2PasswordRequestForm): The login credentials (username as email and password).

    Returns:
        dict: The access token and its type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    logger.info(f"Login endpoint accessed for email: {form_data.username}")

    # Extract credentials
    email = form_data.username  # OAuth2PasswordRequestForm uses 'username' for email
    password = form_data.password

    # Authenticate user
    user = authenticate_user(email, password)
    if not user:
        logger.warning(f"Login failed for email: {email}. Invalid credentials.")
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.info(f"Login successful for email: {email}")

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Protected route: Returns the profile of the currently logged-in user.

    Args:
        current_user (dict): The currently authenticated user (injected by `get_current_user`).

    Returns:
        dict: The user's profile information.

    Raises:
        HTTPException: If the user is not authenticated.
    """
    logger.info(f"Profile endpoint accessed for user: {current_user['username']}")

    # Fetch user details from the database
    user = username_exists(current_user.get("username"))
    if not user:
        logger.warning(
            f"Profile fetch failed: User {current_user['username']} not found."
        )
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    logger.info(f"Profile fetched successfully for user: {current_user['username']}")

    return {
        "message": "This is your profile",
        "user": {
            "email": user["email"],
            "full_name": user["full_name"],
        },
    }
