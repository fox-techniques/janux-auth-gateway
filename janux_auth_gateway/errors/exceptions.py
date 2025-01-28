"""
exceptions.py

Defines custom exception classes for the JANUX Authentication Gateway.

Features:
- AuthenticationError: Raised for authentication-related failures.
- ValidationError: Raised for validation-related failures.
- DatabaseError: Raised for database-related issues.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import HTTPException, status


class AuthenticationError(HTTPException):
    """
    Custom exception for authentication errors.
    """

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ValidationError(HTTPException):
    """
    Custom exception for validation errors.
    """

    def __init__(self, detail: str = "Invalid input provided"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class DatabaseError(HTTPException):
    """
    Custom exception for database errors.
    """

    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )
