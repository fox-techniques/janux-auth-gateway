"""
admin.py

Defines the Admin model for MongoDB using Beanie.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
Date: [Insert Date]
"""

from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone


class Admin(Document):
    """
    Beanie model for the Admin collection in MongoDB.

    Attributes:
        email (EmailStr): The email address of the admin.
        full_name (str): The full name of the admin.
        hashed_password (str): The hashed password for the admin.
        created_at (datetime): The timestamp of when the admin was created.
    """

    email: EmailStr = Field(..., unique=True, example="admin@example.com")
    full_name: str = Field(..., example="Admin User")
    hashed_password: str = Field(..., example="hashed_password_123")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """
        Configuration for the MongoDB collection.
        """

        collection = "admins"

    class Config:
        """
        Pydantic model configuration for JSON serialization and schema.
        """

        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "full_name": "Admin User",
                "hashed_password": "hashed_password_123",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }
