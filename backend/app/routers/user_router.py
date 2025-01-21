from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.database import users_collection
from app.utils.passwords import hash_password
from bson import ObjectId

user_router = APIRouter()


@user_router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    """
    Register a new user. Hash the password and store user details in MongoDB.
    """
    # Check if user already exists
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

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
