"""
mongoDB.py

This module handles MongoDB connections and user authentication operations using Beanie ODM.

Features:
- Connect to MongoDB using a configurable URI.
- Authenticate users by verifying their username and password.
- Query users and admins from the database using Beanie models.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from typing import Optional

from janux_auth_gateway.auth.passwords import verify_password, hash_password
from janux_auth_gateway.config import Config
from janux_auth_gateway.debug.custom_logger import get_logger
from janux_auth_gateway.models.user import User
from janux_auth_gateway.models.admin import Admin

# Initialize logger
logger = get_logger("auth_service_logger")


async def init_db() -> None:
    """
    Initialize the MongoDB database connection with Beanie.

    Raises:
        SystemExit: If the MongoDB server is not reachable or authentication fails.
    """
    try:
        # MongoDB connection URI
        MONGO_URI = Config.MONGO_URI
        client = AsyncIOMotorClient(
            MONGO_URI, serverSelectionTimeoutMS=5000
        )  # 5-second timeout
        db = client[Config.MONGO_DATABASE_NAME]

        # Attempt to connect and list databases (to check connectivity)
        logger.info("Testing MongoDB connection...")
        await client.server_info()  # This raises an exception if the server is unreachable

        # Initialize Beanie with User and Admin models
        await init_beanie(database=db, document_models=[User, Admin])

        logger.info("Connected to MongoDB and initialized Beanie successfully.")
        await ensure_super_admin_exists()

    except ServerSelectionTimeoutError as timeout_error:
        logger.critical("Failed to connect to MongoDB: Timeout reached.")
        logger.critical(f"Error: {timeout_error}")
        raise SystemExit("MongoDB connection timeout. Application cannot start.")

    except OperationFailure as auth_error:
        logger.critical("Failed to authenticate with MongoDB.")
        logger.critical(f"Error: {auth_error}")
        raise SystemExit("MongoDB authentication failed. Application cannot start.")

    except Exception as general_error:
        logger.critical("An unexpected error occurred while connecting to MongoDB.")
        logger.critical(f"Error: {general_error}")
        raise SystemExit(
            "Unexpected error during MongoDB initialization. Application cannot start."
        )


async def ensure_super_admin_exists() -> None:
    """
    Ensure a super admin account exists in the database. Create one if it doesn't.

    Raises:
        ValueError: If required configuration values are missing.
    """
    admin_email = Config.MONGO_SUPER_ADMIN_EMAIL
    admin_password = Config.MONGO_SUPER_ADMIN_PASSWORD

    if not admin_email or not admin_password:
        logger.error("Super admin email or password is not configured.")
        raise ValueError("Super admin email or password is not configured.")

    existing_admin = await Admin.find_one(Admin.email == admin_email)
    if not existing_admin:

        admin = Admin(
            email=admin_email,
            full_name="Super Admin",
            hashed_password=hash_password(admin_password),
            role="super_admin",
        )
        await admin.insert()
        logger.info(f"Default admin account created: {admin_email}")


async def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying their username and password.

    Args:
        username (str): The user's email or username.
        password (str): The user's plain-text password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    logger.info("Authenticating user...")

    try:
        user = await username_exists(username)

        if not user:
            logger.warning("Username does not exist.")
            return False

        if not verify_password(password, user.hashed_password):
            logger.warning("Password verification failed.")
            return False

        logger.info("User authenticated successfully.")
        return True

    except Exception as e:
        logger.error(f"Error during user authentication: {e}")
        return False


async def username_exists(username: str) -> Optional[User]:
    """
    Check if a username exists in the database.

    Args:
        username (str): The user's email or username to search for.

    Returns:
        Optional[User]: The user's data if the username exists, None otherwise.
    """
    logger.info("Checking if username exists...")

    try:
        user = await User.find_one(User.email == username)
        if not user:
            logger.info("Username not found in the database.")
            return None

        logger.info("Username exists in the database.")
        return user
    except Exception as e:
        logger.error(f"Error while checking username existence: {e}")
        return None


async def authenticate_admin(username: str, password: str) -> bool:
    """
    Authenticate an admin by verifying their username and password.

    Args:
        username (str): The admin's email or username.
        password (str): The admin's plain-text password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    logger.info("Authenticating admin...")

    try:
        admin = await admin_username_exists(username)
        if not admin:
            logger.warning("Admin username does not exist.")
            return False

        if not verify_password(password, admin.hashed_password):
            logger.warning("Admin password verification failed.")
            return False

        logger.info("Admin authenticated successfully.")
        return True

    except Exception as e:
        logger.error(f"Error during admin authentication: {e}")
        return False


async def admin_username_exists(username: str) -> Optional[Admin]:
    """
    Check if an admin's username exists in the database.

    Args:
        username (str): The admin's email or username to search for.

    Returns:
        Optional[Admin]: The admin's data if the username exists, None otherwise.
    """
    logger.info("Checking if admin username exists...")

    try:
        admin = await Admin.find_one(Admin.email == username)
        if not admin:
            logger.info("Admin username not found in the database.")
            return None

        logger.info("Admin username exists in the database.")
        return admin
    except Exception as e:
        logger.error(f"Error while checking admin's username existence: {e}")
        return None
