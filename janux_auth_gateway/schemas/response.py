"""
response.py

Defines Pydantic schemas for standardized API responses.

Schemas:
- ConflictResponse: Schema for conflict error responses.
- ErrorResponse: Schema for general error responses.

Features:
- Provides a consistent structure for API error responses.
- Includes example values for better API documentation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field, ConfigDict


class ConflictResponse(BaseModel):
    """
    Schema for conflict error responses.

    Attributes:
        detail (str): A detailed error message.
    """

    detail: str = Field(..., example="Email already registered.")

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "Email already registered."}}
    )


class ErrorResponse(BaseModel):
    """
    Schema for general error responses.

    Attributes:
        detail (str): A detailed error message.
        code (int): The HTTP status code associated with the error.
    """

    detail: str = Field(..., example="An unexpected error occurred.")
    code: int = Field(..., example=500)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "An unexpected error occurred.", "code": 500}
        }
    )
