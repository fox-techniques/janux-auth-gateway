"""
Middleware for adding unique correlation IDs to HTTP requests.

Features:
- Generates a unique request ID for every incoming request.
- Logs the request ID along with request and response details.
- Includes the request ID in the response headers for client tracking.

Benefits:
- Enables easier tracing of individual requests in logs.
- Facilitates debugging in distributed systems.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import Request
from uuid import uuid4
from janux_auth_gateway.debug.custom_logger import get_logger

logger = get_logger("auth_service_logger")


async def add_request_id(request: Request, call_next):
    """
    Middleware to add a unique request ID to every HTTP request.

    Args:
        request (Request): The incoming HTTP request object.
        call_next: Function to call the next middleware or route.

    Returns:
        Response: The HTTP response with a request ID header.
    """
    request_id = str(uuid4())
    logger.info(f"Request {request_id} started: {request.method} {request.url.path}")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    logger.info(f"Request {request_id} completed with status {response.status_code}")
    return response
