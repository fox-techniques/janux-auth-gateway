from fastapi import APIRouter
from app.logging.custom_logger import get_logger

logger = get_logger("app_logger")
base_router = APIRouter()


@base_router.get("/")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the JANUX Backend!"}


@base_router.get("/health")
def health_check():
    logger.info("Health check endpoint accessed.")
    return {"status": "healthy"}
