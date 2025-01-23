from fastapi import Request
from app.logging.custom_logger import get_logger

import time

logger = get_logger("app_logger")


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
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    logger = get_logger("app_logger")
    logger.info(
        f"{request.method} {request.url.path} completed In: {process_time:.2f}ms, Status: {response.status_code}"
    )
    return response
