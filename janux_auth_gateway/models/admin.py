"""
admin.py

Defines the Admin model for MongoDB using Beanie.

Features:
- Stores admin details such as email, full name, hashed password, and role.
- Supports role-based control using `AdminRole` enum.
- Automatically sets the creation timestamp for new admins.
- Includes validation for fields such as `full_name`.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import EmailStr, Field
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
    full_name: str = Field(..., example="Admin User")
    hashed_password: str = Field(..., example="hashed_password_123")
    role: AdminRole = Field(default=AdminRole.ADMIN, example="admin")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def validate_full_name(cls, value: str) -> str:
        """
        Validates the full name field.

        Args:
            value (str): The full name of the admin.

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
        String representation of the Admin instance.

        Returns:
            str: A string representing the admin's details.
        """
        return (
            f"Admin(email={self.email}, role={self.role}, created_at={self.created_at})"
        )
