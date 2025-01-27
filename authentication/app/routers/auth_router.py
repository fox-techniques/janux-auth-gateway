from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from starlette import status
from app.auth.jwt import create_access_token
from app.database.mongoDB import authenticate_user, authenticate_admin
from app.config import Config
from app.schemas.token import Token

auth_router = APIRouter()


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Unified login endpoint for both users and admins.
    """
    email = form_data.username
    password = form_data.password

    if await authenticate_admin(email, password):
        role = "admin"
    elif await authenticate_user(email, password):
        role = "user"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": email, "role": role},
        expires_delta=timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")
