from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from starlette import status

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")


def register_error_handlers(app: FastAPI):
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": "An unexpected error occurred."},
        )


async def http_exception_handler(request: Request, exc: Exception):
    """
    Exception handler for HTTP exceptions raised during request processing.

    This handler logs the exception details and returns a JSON response containing the error message and HTTP status code.
    This standardizes error responses across the application.

    Args:
        request (Request): The request object during which the exception occurred.
        exc (HTTPException): The exception instance containing details about the HTTP error.

    Returns:
        JSONResponse: A JSON response that includes the error detail and the HTTP status code.
    """
    # Log the exception
    logger.error(f"Exception occurred: {str(exc)}", exc_info=True)

    # Return a generic error response if detail is missing
    detail = getattr(exc, "detail", "An unexpected error occurred")
    status_code = getattr(exc, "status_code", 500)

    return JSONResponse(
        content={"detail": detail},
        status_code=status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Exception handler for handling validation errors raised when request data does not fulfill the expected schema.

    This function logs the validation issues and returns a JSON response that details the validation errors,
    using a 422 Unprocessable Entity status code. This informs the client about the incorrect or missing data in the request.

    Args:
        request (Request): The request object during which the validation error occurred.
        exc (RequestValidationError): The exception instance that includes detailed validation error information.

    Returns:
        JSONResponse: A response containing the detailed validation errors and a 422 status code.
    """
    logger.warning(f"Validation Error: {exc}", exc_info=True)
    return JSONResponse(content={"detail": exc.errors()}, status_code=422)
