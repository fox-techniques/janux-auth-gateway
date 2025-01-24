"""
user_router.py

Defines user-related API routes, including registration, login, and profile retrieval.

Endpoints:
- `/register`: Register a new user.
- `/login`: Authenticate a user and return a JWT token.
- `/logout`: Log out the currently authenticated user.
- `/profile`: Retrieve the profile of the currently authenticated user.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from datetime import timedelta

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.response import ConflictResponse
from app.auth.passwords import hash_password, verify_password
from app.auth.jwt import create_access_token, get_current_user
from app.models.user import User
from app.config import Config
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")


# OAuth2 Bearer configuration
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

# Initialize router
user_router = APIRouter()

# In-memory token blacklist (replace with a persistent store in production)
TOKEN_BLACKLIST = set()


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
    existing_user = await User.find_one(User.email == user.email)
    if existing_user:
        logger.warning(f"Registration failed: Email {user.email} already registered.")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered.",
        )

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create and insert the user into the database
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    await new_user.insert()

    logger.info(f"User registered successfully with email: {user.email}")

    # Return the created user
    return UserResponse(
        id=str(new_user.id), email=new_user.email, full_name=new_user.full_name
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
    user = await User.find_one(User.email == email)

    if not user or not verify_password(password, user.hashed_password):
        logger.warning(f"Login failed for email: {email}. Invalid credentials.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
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


@user_router.post("/logout")
async def logout_user(
    current_user: dict = Depends(get_current_user), token: str = Depends(oauth2_bearer)
):
    """
    Log out the currently authenticated user by marking their token as invalid.

    Args:
        current_user (dict): The currently authenticated user.
        token (str): The JWT token to invalidate.

    Returns:
        dict: A confirmation message.
    """
    logger.info(f"Logout endpoint accessed by user: {current_user['username']}")

    # Add token to the blacklist (in-memory or persistent store)
    TOKEN_BLACKLIST.add(token)
    logger.info(f"Token invalidated for user: {current_user['username']}")

    return {"message": "Successfully logged out. You can log back in anytime."}


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
    user = await User.find_one(User.email == current_user["username"])
    if not user:
        logger.warning(
            f"Profile fetch failed: User {current_user['username']} not found."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    logger.info(f"Profile fetched successfully for user: {current_user['username']}")

    return {
        "message": "This is your profile",
        "user": {
            "email": user.email,
            "full_name": user.full_name,
        },
    }
