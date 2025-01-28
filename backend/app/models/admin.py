"""
admin.py

Defines the Admin model for MongoDB using Beanie.

Features:
- Stores admin details such as email, full name, hashed password, and role.
- Automatically sets the creation timestamp for new admins.
- Uses unique constraints and Pydantic for validation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field
from datetime import datetime, timezone
from typing import Literal


class Admin(Document):
    """
    Beanie model for the Admin collection in MongoDB.

    Attributes:
        email (EmailStr): The email address of the admin.
        full_name (str): The full name of the admin.
        hashed_password (str): The hashed password for the admin.
        role (Literal): The role of the admin user (e.g., "admin", "super_admin").
        created_at (datetime): The timestamp of when the admin was created.
    """

    email: EmailStr = Field(..., unique=True, example="admin@example.com")
    full_name: str = Field(..., example="Admin User")
    hashed_password: str = Field(..., example="hashed_password_123")
    role: Literal["admin", "super_admin"] = Field(default="admin", example="admin")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """
        Settings for the MongoDB collection for admins.
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
                "role": "admin",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }

    def __str__(self) -> str:
        """
        String representation of the Admin instance for logging and debugging.

        Returns:
            str: A string representing the admin's email and role.
        """
        return f"Admin(email={self.email}, role={self.role})"
