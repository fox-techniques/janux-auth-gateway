"""
main.py

Entry point for the JANUX Authentication microservice. This file initializes the FastAPI app, sets up middleware,
exception handlers, routes, and establishes the MongoDB connection using Beanie.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
Date: [Insert Date]
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.errors.handlers import register_error_handlers
from app.logging.requests import log_requests
from app.routers.base_router import base_router
from app.routers.user_router import user_router
from app.logging.custom_logger import get_logger

# Initialize the logger
logger = get_logger("app_logger")
logger.info("--- JANUX Authentication service starts here ------------------------")


def lifespan(app: FastAPI):
    """
    Lifespan context for application startup and shutdown events.

    Logs application startup and shutdown messages. Utilizes an async generator
    to handle lifecycle events efficiently.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("JANUX Authentication application is starting up...")
    yield
    logger.info("JANUX Authentication application is shutting down...")


# Create the FastAPI application instance
app = FastAPI(title="JANUX Authentication Microservice", lifespan=lifespan)

# Configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production environments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
app.middleware("http")(log_requests)

# Register exception handlers
register_error_handlers(app)

# Register application routes
app.include_router(base_router, tags=["Default"])
app.include_router(user_router, prefix="/users", tags=["Users"])


# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn

    logger.info("Running JANUX Authentication application using __main__")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
