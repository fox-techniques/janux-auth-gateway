"""
response.py

Defines Pydantic schemas for standardized API responses.

Schemas:
- ConflictResponse: Schema for conflict error responses.
- ErrorResponse: Schema for general error responses.
- UnauthorizedResponse: Schema for authentication error responses.

Features:
- Provides a consistent structure for API error responses.
- Includes example values for better API documentation.
- Ensures structured responses for unauthorized access errors.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field, ConfigDict


class ConflictResponse(BaseModel):
    """
    Schema for conflict error responses.

    Attributes:
        detail (str): A detailed error message.
    """

    detail: str = Field(..., json_schema_extra={"example": "Email already registered."})

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

    detail: str = Field(
        ..., json_schema_extra={"example": "An unexpected error occurred."}
    )
    code: int = Field(..., json_schema_extra={"example": 500})

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"detail": "An unexpected error occurred.", "code": 500}
        }
    )


class UnauthorizedResponse(BaseModel):
    """
    Schema for authentication error responses.

    Attributes:
        detail (str): A message explaining the authentication failure.
        code (int): The HTTP status code for unauthorized errors.
    """

    detail: str = Field(..., json_schema_extra={"example": "Invalid credentials."})
    code: int = Field(..., json_schema_extra={"example": 401})

    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "Invalid credentials.", "code": 401}}
    )
