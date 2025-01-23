"""
user.py

Defines Pydantic schemas for user-related operations.

Schemas:
- `UserBase`: Base schema for user details.
- `UserCreate`: Schema for user registration.
- `UserResponse`: Schema for user response data.
- `UserLogin`: Schema for user login credentials.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Base schema for user details.

    Attributes:
        email (EmailStr): The email address of the user.
        full_name (str): The full name of the user.
    """

    email: EmailStr = Field(..., example="john.smith@janux.com")
    full_name: str = Field(..., example="John Smith")


class UserCreate(UserBase):
    """
    Schema for user registration.

    Extends:
        UserBase

    Attributes:
        password (str): The plain-text password for the user.
    """

    password: str = Field(..., min_length=8, example="SecurePassword123!")


class UserResponse(UserBase):
    """
    Schema for user response data.

    Extends:
        UserBase

    Attributes:
        id (str): The unique identifier for the user.
    """

    id: str = Field(..., example="507f1f77bcf86cd799439011")


class UserLogin(BaseModel):
    """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The email address of the user.
        password (str): The plain-text password for the user.
    """

    email: EmailStr = Field(..., example="john.smith@janux.com")
    password: str = Field(..., min_length=8, example="SecurePassword123!")
