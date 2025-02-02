"""
user.py

Defines the User model for MongoDB using Beanie.

Features:
- Stores user details such as email, full name, hashed password, and role.
- Supports role-based control using `UserRole` enum.
- Automatically sets the creation timestamp for new users.
- Includes validation for fields such as `email`, `full_name`, and `hashed_password`.
- Enforces unique email addresses at the database level.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document, Indexed
from pydantic import EmailStr, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from .roles_model import UserRole


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

    email: EmailStr = Indexed(
        EmailStr, unique=True
    )  # Ensure uniqueness in the database
    full_name: str = Field(
        ..., min_length=3, max_length=100, json_schema_extra={"example": "Jane Doe"}
    )
    hashed_password: str = Field(
        ..., min_length=8, json_schema_extra={"example": "hashed_password_123"}
    )
    role: UserRole = Field(default=UserRole.USER, json_schema_extra={"example": "user"})
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        """
        Validates the full name field.

        Raises:
            ValueError: If the full name is empty or too short.
        """
        if not value.strip():
            raise ValueError("Full name cannot be empty.")
        if len(value) < 3:
            raise ValueError("Full name must be at least 3 characters long.")
        return value

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        """
        Validates the hashed password.

        Raises:
            ValueError: If the password is too short.
        """
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jane.doe@example.com",
                "full_name": "Jane Doe",
                "hashed_password": "hashed_password_123",
                "role": "user",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }
    )

    def __str__(self) -> str:
        """
        String representation of the User instance.
        """
        return (
            f"User(email={self.email}, role={self.role}, created_at={self.created_at})"
        )
