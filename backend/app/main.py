from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.errors.handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.logging.requests import log_requests
from app.routers import base_router
from app.routers.user_router import user_router

from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")
logger.info("--- JANUX Backend starts here ------------------------ ")


async def lifespan(app: FastAPI):
    """
    Lifespan context for application startup and shutdown events.
    This function uses an async generator to handle lifecycle events.
    """
    logger.info("Application is starting up...")
    yield  # This is required for FastAPI's lifespan implementation
    logger.info("Application is shutting down...")


# Create FastAPI instance with lifespan
app = FastAPI(title="JANUX Backend", lifespan=lifespan)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)

# Exception Handlers
app.add_exception_handler(Exception, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Routes
app.include_router(base_router)
app.include_router(user_router, prefix="/users", tags=["Users"])

# Add __main__ block
if __name__ == "__main__":
    import uvicorn

    logger.info("Running application using __main__")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
