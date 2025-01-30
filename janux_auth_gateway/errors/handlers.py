"""
handlers.py

Provides custom exception handlers for the FastAPI application.

Features:
- Handles unexpected exceptions (500 Internal Server Error).
- Handles custom exceptions like AuthenticationError, ValidationError, and DatabaseError.
- Logs detailed error information for debugging.
- Registers exception handlers with the FastAPI app.
- Ensures the application does not fail due to missing configuration attributes.

Usage:
- Call `register_error_handlers(app)` during FastAPI app initialization.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
import traceback
from janux_auth_gateway.config import Config
from janux_auth_gateway.debug.custom_logger import get_logger
from janux_auth_gateway.errors.exceptions import (
    AuthenticationError,
    ValidationError,
    DatabaseError,
)

logger = get_logger("auth_service_logger")


def register_error_handlers(app: FastAPI):
    """
    Register custom error handlers with the FastAPI application.
    """

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handle unexpected exceptions and log them.
        """
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        response = {"message": "An unexpected error occurred."}

        # Ensure DEBUG attribute exists before accessing it
        if getattr(Config, "DEBUG", False):
            response["traceback"] = traceback.format_exc()

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response,
        )

    @app.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, exc: AuthenticationError):
        """
        Handle authentication errors.
        """
        logger.warning(f"Authentication error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    @app.exception_handler(ValidationError)
    async def validation_error_handler(request: Request, exc: ValidationError):
        """
        Handle validation errors.
        """
        logger.warning(f"Validation error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Handle request validation errors.
        """
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"message": "Validation failed.", "errors": exc.errors()},
        )

    @app.exception_handler(DatabaseError)
    async def database_error_handler(request: Request, exc: DatabaseError):
        """
        Handle database errors.
        """
        logger.error(f"Database error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    # Register handlers for specific exceptions
    app.add_exception_handler(AuthenticationError, authentication_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(DatabaseError, database_error_handler)

    # Register handler for generic exceptions
    app.add_exception_handler(Exception, generic_exception_handler)
