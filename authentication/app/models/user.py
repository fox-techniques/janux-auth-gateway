"""
user.py

Defines the User model for MongoDB using Beanie.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone


class User(Document):
    """
    Beanie model for the User collection in MongoDB.
    """

    email: EmailStr = Field(..., unique=True, example="john.smith@janux.com")
    full_name: str = Field(..., example="John Smith")
    hashed_password: str = Field(..., example="hashed_password_123")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """
        Settings for the User collection.
        """

        collection = "users"

    class Config:
        """
        Pydantic model configuration.
        """

        schema_extra = {
            "example": {
                "email": "john.smith@janux.com",
                "full_name": "John Smith",
                "hashed_password": "hashed_password_123",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }
