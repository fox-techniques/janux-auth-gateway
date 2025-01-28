"""
errors module

Comprehensive error handling for the JANUX Authentication Gateway.

Submodules:
- handlers: Registers exception handlers for common and custom errors.
- exceptions: Defines custom exceptions for more granular error handling.

Features:
- Handles unexpected exceptions and provides structured responses.
- Custom exceptions for authentication, validation, and database errors.
- Debug-friendly error responses during development.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .handlers import register_error_handlers
from .exceptions import AuthenticationError, ValidationError, DatabaseError

__all__ = [
    "register_error_handlers",
    "AuthenticationError",
    "ValidationError",
    "DatabaseError",
]
