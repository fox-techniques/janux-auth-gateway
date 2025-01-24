"""
user.py

Defines the User model for MongoDB using Beanie, with support for roles.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Literal


class User(Document):
    """
    Beanie model for the User collection in MongoDB.

    Attributes:
        email (EmailStr): The email address of the user.
        full_name (str): The full name of the user.
        hashed_password (str): The hashed password for the user.
        role (str): The role of the user (e.g., "user", "admin").
        created_at (datetime): The timestamp of when the user was created.
    """

    email: EmailStr = Field(..., unique=True, example="john.smith@janux.com")
    full_name: str = Field(..., example="John Smith")
    hashed_password: str = Field(..., example="hashed_password_123")
    role: Literal["user", "admin"] = Field(default="user", example="user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """
        Settings for the MongoDB collection for users.
        """

        collection = "users"

    class Config:
        """
        Pydantic model configuration for JSON serialization and schema.
        """

        json_schema_extra = {
            "example": {
                "email": "john.smith@janux.com",
                "full_name": "John Smith",
                "hashed_password": "hashed_password_123",
                "role": "user",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }
