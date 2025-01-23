"""
response.py

Defines Pydantic schemas for standardized API responses.

Schemas:
- `ConflictResponse`: Schema for conflict error responses.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field


class ConflictResponse(BaseModel):
    """
    Schema for conflict error responses.

    Attributes:
        detail (str): A detailed error message.
    """

    detail: str = Field(..., example="Email already registered.")
