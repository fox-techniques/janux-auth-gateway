"""
handlers.py

Custom error handlers for the FastAPI application.

Features:
- Handles unexpected exceptions (500 Internal Server Error).
- Handles HTTP exceptions and validation errors consistently.
- Logs detailed error information for debugging.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")


def register_error_handlers(app: FastAPI) -> None:
    """
    Register custom error handlers with the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Handle unexpected exceptions and log them.

        Args:
            request (Request): The request object.
            exc (Exception): The exception instance.

        Returns:
            JSONResponse: A 500 Internal Server Error response.
        """
        logger.error(
            f"Unexpected error occurred: {str(exc)}",
            exc_info=True,
            extra={"path": request.url.path, "method": request.method},
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred."},
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """
        Handle HTTP exceptions and return a JSON response.

        Args:
            request (Request): The request object.
            exc (HTTPException): The exception instance containing HTTP error details.

        Returns:
            JSONResponse: A response with the HTTP status code and error details.
        """
        logger.warning(
            f"HTTP Exception: {exc.detail}",
            extra={"path": request.url.path, "method": request.method},
        )
        return JSONResponse(
            content={"detail": exc.detail},
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        """
        Handle validation errors and return detailed error messages.

        Args:
            request (Request): The request object.
            exc (RequestValidationError): The exception instance containing validation error details.

        Returns:
            JSONResponse: A 422 Unprocessable Entity response with validation errors.
        """
        logger.warning(
            f"Validation Error: {exc.errors()}",
            extra={"path": request.url.path, "method": request.method},
        )
        return JSONResponse(
            content={"detail": exc.errors()},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # Register the handlers
    app.add_exception_handler(Exception, generic_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
