from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.response import ConflictResponse

from fastapi.security import OAuth2PasswordRequestForm

from app.auth.passwords import hash_password
from app.database.mongoDB import authenticate_user, username_exists, users_collection

from app.auth.jwt import create_access_token
from datetime import timedelta

from starlette import status
from fastapi import APIRouter, Depends
from app.auth.jwt import get_current_user

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")

ACCESS_TOKEN_EXPIRE_MINUTES = 20

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
    """
    logger.info("Register endpoint accessed.")

    # Check if user already exists
    existing_user = username_exists(user.email)
    if existing_user:
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

    # Return the created user
    return UserResponse(
        id=str(result.inserted_id), email=user.email, full_name=user.full_name
    )


@user_router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in a user by validating their credentials and generating a JWT token.
    """
    logger.info("Login endpoint accessed.")

    # Extract credentials from form_data
    email = form_data.username  # OAuth2PasswordRequestForm uses 'username' for email
    password = form_data.password

    # Authenticate user
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@user_router.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Protected route: Returns the profile of the currently logged-in user.
    """
    logger.info("Profile endpoint accessed.")

    return {"message": "This is your profile", "user": current_user}
