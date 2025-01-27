"""
base_router.py

Defines the base API routes for the JANUX Authentication microservice.

Endpoints:
- `/`: Root endpoint to welcome users.
- `/health`: Health check endpoint to verify service status.

Features:
- Lightweight and essential routes for service interaction.
- Provides a health check mechanism to monitor service availability.
- Detailed logging for basic interactions.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# Initialize the router
base_router = APIRouter()


@base_router.get("/")
async def root():
    """
    Root endpoint to welcome users to the JANUX Authentication microservice.

    Returns:
        dict: A welcome message.
    """
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the JANUX Authentication microservice!"}


@base_router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service status.

    Returns:
        dict: The health status of the service.
    """
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}
