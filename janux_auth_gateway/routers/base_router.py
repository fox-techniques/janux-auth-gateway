"""
base_router.py

Defines the base API routes for the JANUX Authentication Gateway.

Endpoints:
- `/`: Root endpoint to welcome users.
- `/health`: Health check endpoint to verify service status.

Features:
- Lightweight and essential routes for service interaction.
- Provides a health check mechanism to monitor service availability.
- Logs API accesses for better monitoring and debugging.
- Ensures readiness and liveness probes for containerized environments.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Initialize the router
base_router = APIRouter()


@base_router.get("/")
async def root():
    """
    Root endpoint to welcome users to the JANUX Authentication Gateway.

    Returns:
        dict: A welcome message.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the JANUX Authentication Gateway!"}


@base_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service status.

    Returns:
        dict: The health status of the service.
    """
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}


@base_router.get("/readiness")
async def readiness_probe():
    """
    Readiness probe to indicate if the application is ready to receive traffic.

    Returns:
        dict: The readiness status.
    """
    logger.info("Readiness probe accessed.")
    return {"status": "ready"}


@base_router.get("/liveness")
async def liveness_probe():
    """
    Liveness probe to check if the application is running properly.

    Returns:
        dict: The liveness status.
    """
    logger.info("Liveness probe accessed.")
    return {"status": "alive"}
