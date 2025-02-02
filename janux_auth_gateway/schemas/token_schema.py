"""
token.py

Defines Pydantic schema for token-related data.

Schemas:
- Token: Represents an access token with a type.
- TokenPayload: Represents decoded JWT token payload details.

Features:
- Provides standardized representation of JWT tokens.
- Includes example values for better API documentation.
- Adds a schema for decoding and validating token payloads.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class Token(BaseModel):
    """
    Schema for access token data.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str = Field(
        ..., json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}
    )
    token_type: str = Field(..., json_schema_extra={"example": "bearer"})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    )


class TokenPayload(BaseModel):
    """
    Schema for decoded JWT token payload.

    Attributes:
        sub (str): Subject (user email or identifier).
        role (str): The role assigned to the user.
        exp (Optional[int]): Expiration time of the token.
    """

    sub: str = Field(..., json_schema_extra={"example": "user@example.com"})
    role: str = Field(..., json_schema_extra={"example": "user"})
    exp: Optional[int] = Field(None, json_schema_extra={"example": 1678901234})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sub": "user@example.com",
                "role": "user",
                "exp": 1678901234,
            }
        }
    )
