"""
main.py

Entry point for the JANUX Feedback microservice. This file initializes the FastAPI app, sets up middleware,
exception handlers, routes, and establishes the MongoDB connection using Beanie.


Features:
- Middleware for request logging.
- Custom exception handlers for consistent error responses.
- Modular route inclusion for base, auth, user, and admin APIs.
- MongoDB initialization with Beanie ODM.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.errors.handlers import register_error_handlers
from app.logging.requests import log_requests
from app.routers.base_router import base_router
from app.routers.feedback_router import feedback_router
from app.database.mongoDB import init_db
from app.logging.custom_logger import get_logger

# Initialize the logger
logger = get_logger("feedback_service_logger")
logger.info("--- JANUX Feedback service starts here ------------------------")


async def lifespan(app: FastAPI):
    """
    Lifespan context for application startup and shutdown events.

    Logs application startup and shutdown messages. Utilizes an async generator
    to handle lifecycle events efficiently.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """
    logger.info("Feedback Service Application is starting up...")

    # Initialize database connection
    logger.info("Initializing database connection...")
    await init_db()
    yield
    logger.info("Feedback Service Application is shutting down...")


# Create the FastAPI application instance
app = FastAPI(title="Feedback Microservice", lifespan=lifespan)

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
app.include_router(feedback_router, prefix="/feedback", tags=["Feedback"])

# Run the application if executed directly
if __name__ == "__main__":
    import uvicorn

    logger.info("Running Feedback service using __main__")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)
