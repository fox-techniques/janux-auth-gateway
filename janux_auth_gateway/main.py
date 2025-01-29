"""
main.py

Entry point for the JANUX Authentication Gateway.

This file initializes the FastAPI app, sets up middleware, exception handlers, 
routes, and establishes the MongoDB connection using Beanie.

Features:
- Middleware for request logging and correlation IDs.
- Centralized error handling for consistent API responses.
- Modular route inclusion for base, auth, user, and admin APIs.
- MongoDB initialization with Beanie ODM.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from janux_auth_gateway.errors.handlers import register_error_handlers
from janux_auth_gateway.debug.requests import log_requests
from janux_auth_gateway.debug.middleware import add_request_id
from janux_auth_gateway.routers.base_router import base_router
from janux_auth_gateway.routers.user_router import user_router
from janux_auth_gateway.routers.admin_router import admin_router
from janux_auth_gateway.routers.auth_router import auth_router
from janux_auth_gateway.config import Config
from janux_auth_gateway.database.mongoDB import init_db
from janux_auth_gateway.debug.custom_logger import get_logger


import os

logger = get_logger("auth_service_logger")


async def lifespan(app: FastAPI):
    """
    Lifespan context for application startup and shutdown events.

    Logs application startup and shutdown messages. If MongoDB initialization
    fails, the application will exit with an appropriate message.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    try:
        logger.info("JANUX Authentication Application is starting up...")

        environment = Config.ENVIRONMENT
        containerized = Config.CONTAINER

        logger.info(f"Running in environment: {environment}")
        logger.info(f"Containerized environment: {containerized}")

        if containerized:
            logger.info("Detected containerized environment.")
        else:
            logger.info("Running in local development mode.")

        # Initialize MongoDB connection
        logger.info("Initializing database connection...")
        await init_db()

        yield  # Application is running

    except SystemExit as critical_error:
        logger.critical(f"Critical error during startup: {critical_error}")
        raise critical_error

    except Exception as unexpected_error:
        logger.critical(f"Unexpected error during startup: {unexpected_error}")
        raise unexpected_error

    finally:
        logger.info("JANUX Authentication Application is shutting down...")


# Create the FastAPI application instance
app = FastAPI(title="JANUX Authentication Gateway", lifespan=lifespan)

# Configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)
app.middleware("http")(add_request_id)

# Register exception handlers
register_error_handlers(app)

# Register application routes
app.include_router(base_router, tags=["Default"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(admin_router, prefix="/admins", tags=["Admins"])
app.include_router(user_router, prefix="/users", tags=["Users"])

# Entry point for running the app directly
if __name__ == "__main__":
    import uvicorn

    logger.info("Running JANUX Authentication Gateway as a standalone application...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
