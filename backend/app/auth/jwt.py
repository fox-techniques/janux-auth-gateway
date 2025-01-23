from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from starlette import status

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")

# Constants
SECRET_KEY = "your-secret-key"  # Use a strong secret key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create a JWT token with optional expiration time using timezone-aware UTC datetime.
    """
    logger.info("Creating access token...")

    to_encode = data.copy()

    if expires_delta:
        expires = datetime.now(timezone.utc) + expires_delta
    else:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    to_encode.update({"exp": expires})

    # Add a unique identifier for the token (e.g., "jti")
    to_encode["jti"] = f"token-{datetime.now(timezone.utc).timestamp()}"
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_bearer)):
    logger.info("Getting current user...")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")

        if not username or not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user",
            )

        return {"username": username, "id": user_id}

    except JWTError as e:
        logger.error(f"JWT decoding error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
