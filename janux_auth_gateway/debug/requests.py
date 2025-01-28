"""
requests.py

Middleware for logging HTTP request details in a FastAPI application.

Features:
- Logs incoming HTTP requests, including method and path.
- Measures and logs execution time for each request.
- Handles and logs exceptions during request processing.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import Request
from janux_auth_gateway.debug.custom_logger import get_logger

import time

logger = get_logger("auth_service_logger")


async def log_requests(request: Request, call_next):
    """
    Middleware to log the details of every HTTP request processed by the application.

    This function logs the HTTP method, request path, execution time in milliseconds, and the status code of the response.
    This information is crucial for monitoring API performance and debugging.

    Args:
        request (Request): The incoming request object.
        call_next: A function that calls the next item in the middleware stack.

    Returns:
        Response: The response object generated after processing the request.
    """
    start_time = time.time()

    logger.info(f"Request received: {request.method} {request.url.path}")

    try:
        response = await call_next(request)
    except Exception as exc:
        process_time = (time.time() - start_time) * 1000
        logger.error(
            f"Request failed: {request.method} {request.url.path} after {process_time:.2f}ms. Error: {exc}"
        )
        raise

    process_time = (time.time() - start_time) * 1000
    logger.info(
        f"Request completed: {request.method} {request.url.path} in {process_time:.2f}ms. Status: {response.status_code}"
    )

    return response
