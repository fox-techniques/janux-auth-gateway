"""
token.py

Defines Pydantic schema for token-related data.

Schemas:
- `Token`: Schema for access tokens.

Features:
- Standardized representation of JWT tokens.
- Example values for better API documentation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Schema for access token data.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of the token (e.g., "bearer").
    """

    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., example="bearer")
