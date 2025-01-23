# from fastapi import APIRouter, Depends, HTTPException
# from app.schemas.token import Token

# from app.auth.passwords import authenticate_user

# from app.auth.jwt import create_access_token

# from starlette import status

# from fastapi.security import OAuth2PasswordRequestForm

# auth_router = APIRouter()


# @auth_router.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     """
#     Log in a user by validating their credentials and generating a JWT token.
#     """
#     # Find the user in the database
#     user = authenticate_user(form_data.username, form_data.password)

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
#         )

#     # Create an access token
#     access_token = create_access_token(data={"sub": user.email, "id": str(user["_id"])})
#     return {"access_token": access_token, "token_type": "bearer"}
