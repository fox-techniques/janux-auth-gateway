"""
mongoDB.py

This module handles MongoDB connections and user authentication operations.

Features:
- Connect to MongoDB using a configurable URI.
- Authenticate users by verifying their username and password.
- Query users from the database.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure

from app.auth.passwords import verify_password
from app.config import Config
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# MongoDB connection URI (from configuration)
MONGO_URI = Config.MONGO_URI

try:
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client["janux_db"]
    users_collection = db["users"]
    logger.info("Connected to MongoDB successfully.")
except ServerSelectionTimeoutError as se:
    logger.error(f"MongoDB server selection failed: {se}")
    raise
except OperationFailure as oe:
    logger.error(f"MongoDB authentication failed: {oe}")
    raise


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying their username and password.

    Args:
        username (str): The user's email or username.
        password (str): The user's plain-text password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    logger.info("Authenticating user...")

    # Check if the username exists in the database
    user = username_exists(username)
    if not user:
        logger.warning("Username does not exist.")
        return False

    # Check if the password matches the hashed password in the database
    if not verify_password(password, user["password"]):
        logger.warning("Password verification failed.")
        return False

    logger.info("User authenticated successfully.")
    return True


def username_exists(username: str) -> dict:
    """
    Check if a username exists in the database.

    Args:
        username (str): The user's email or username to search for.

    Returns:
        dict: The user's data if the username exists, None otherwise.
    """
    logger.info("Checking if username exists...")

    try:
        # Find the user in the database
        user = users_collection.find_one({"email": username})
        if not user:
            logger.info("Username not found in the database.")
            return None

        logger.info("Username exists in the database.")
        return user
    except Exception as e:
        logger.error(f"Error while checking username existence: {e}")
        return None
