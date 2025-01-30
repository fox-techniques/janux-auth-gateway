"""
admin.py

Defines the Admin model for MongoDB using Beanie.

Features:
- Stores admin details such as email, full name, hashed password, and role.
- Supports role-based control using `AdminRole` enum.
- Automatically sets the creation timestamp for new admins.
- Includes validation for fields such as `email`, `full_name`, and `hashed_password`.
- Enforces unique email addresses at the database level.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field, field_validator, ConfigDict
from datetime import datetime, timezone
from .roles import AdminRole


class Admin(Document):
    """
    Beanie model for the Admin collection in MongoDB.

    Attributes:
        email (EmailStr): The email address of the admin.
        full_name (str): The full name of the admin.
        hashed_password (str): The hashed password for the admin.
        role (AdminRole): The role of the admin user (e.g., "admin", "super_admin").
        created_at (datetime): The timestamp of when the admin was created.
    """

    email: EmailStr = Field(..., unique=True, example="admin@example.com")
    full_name: str = Field(..., min_length=3, max_length=100, example="Admin User")
    hashed_password: str = Field(..., min_length=8, example="hashed_password_123")
    role: AdminRole = Field(default=AdminRole.ADMIN, example="admin")
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
                "email": "admin@example.com",
                "full_name": "Admin User",
                "hashed_password": "hashed_password_123",
                "role": "admin",
                "created_at": "2025-01-23T12:00:00Z",
            }
        }
    )

    class Settings:
        """
        Settings for the MongoDB collection for admins.
        """

        collection_name = "admins"

    def __str__(self) -> str:
        """
        String representation of the Admin instance.
        """
        return (
            f"Admin(email={self.email}, role={self.role}, created_at={self.created_at})"
        )
