"""
user.py

Defines the User model for MongoDB using Beanie.

Features:
- Stores user details such as email, full name, hashed password, and role.
- Supports role-based control using `UserRole` enum.
- Automatically sets the creation timestamp for new users.
- Includes validation for fields such as `full_name`.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field, validator
from datetime import datetime, timezone
from .roles import UserRole


class User(Document):
    """
    Beanie model for the User collection in MongoDB.

    Attributes:
        email (EmailStr): The email address of the user.
        full_name (str): The full name of the user.
        hashed_password (str): The hashed password for the user.
        role (UserRole): The role of the user (e.g., "user", "contributor").
        created_at (datetime): The timestamp of when the user was created.
    """

    email: EmailStr = Field(..., unique=True, example="jane.doe@example.com")
    full_name: str = Field(..., example="Jane Doe")
    hashed_password: str = Field(..., example="hashed_password_123")
    role: UserRole = Field(default=UserRole.USER, example="user")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @validator("full_name")
    def validate_full_name(cls, value: str) -> str:
        """
        Validates the full name field.

        Args:
            value (str): The full name of the user.

        Returns:
            str: The validated full name.

        Raises:
            ValueError: If the full name is empty or invalid.
        """
        if not value.strip():
            raise ValueError("Full name cannot be empty.")
        return value

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
                "email": "jane.doe@example.com",
                "full_name": "Jane Doe",
                "hashed_password": "hashed_password_123",
                "role": "user",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }

    def __str__(self) -> str:
        """
        String representation of the User instance.

        Returns:
            str: A string representing the user's details.
        """
        return (
            f"User(email={self.email}, role={self.role}, created_at={self.created_at})"
        )
