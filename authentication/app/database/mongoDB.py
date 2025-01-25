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

from app.auth.passwords import verify_password
from app.config import Config
from app.logging.custom_logger import get_logger
from app.models.user import User
from app.models.admin import Admin


# Initialize logger
logger = get_logger("app_logger")


async def init_db():
    """
    Initialize the MongoDB database connection with Beanie.
    """
    try:
        # MongoDB connection URI (from configuration)
        MONGO_URI = Config.MONGO_URI
        client = AsyncIOMotorClient(MONGO_URI)
        db = client[Config.MONGO_DATABASE_NAME]

        # Initialize Beanie with the User and Admin models
        await init_beanie(database=db, document_models=[User, Admin])

        logger.info("Connected to MongoDB and initialized Beanie successfully.")

        # Ensure at least one admin exists
        admin_email = Config.MONGO_SUPER_ADMIN_EMAIL
        existing_admin = await Admin.find_one(Admin.email == admin_email)
        if not existing_admin:
            from app.auth.passwords import hash_password

            admin = Admin(
                email=admin_email,
                full_name="Super Admin",
                hashed_password=hash_password(Config.MONGO_SUPER_ADMIN_PASSWORD),
                role="super_admin",
            )
            await admin.insert()
            logger.info(f"Default admin account created: {admin_email}")

    except ServerSelectionTimeoutError as se:
        logger.error(f"MongoDB server selection failed: {se}")
        raise
    except OperationFailure as oe:
        logger.error(f"MongoDB authentication failed: {oe}")
        raise


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

    # Check if the username exists in the database
    user = await username_exists(username)

    if not user:
        logger.warning("Username does not exist.")
        return False

    # Check if the password matches the hashed password in the database
    if not verify_password(password, user.hashed_password):
        logger.warning("Password verification failed.")
        return False

    logger.info("User authenticated successfully.")
    return True


async def username_exists(username: str) -> User:
    """
    Check if a username exists in the database.

    Args:
        username (str): The user's email or username to search for.

    Returns:
        User: The user's data if the username exists, None otherwise.
    """
    logger.info("Checking if username exists...")

    try:
        # Find the user in the database using Beanie
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

    # Check if the username exists in the database
    user = await admin_username_exists(username)
    if not user:
        logger.warning("Admin username does not exist.")
        return False

    # Check if the password matches the hashed password in the database
    if not verify_password(password, user.hashed_password):
        logger.warning("Admin password verification failed.")
        return False

    logger.info("Admin authenticated successfully.")
    return True


async def admin_username_exists(username: str) -> Admin:
    """
    Check if an admin's username exists in the database.

    Args:
        username (str): The admin's email or username to search for.

    Returns:
        Admin: The admin's data if the username exists, None otherwise.
    """
    logger.info("Checking if admin username exists...")

    try:
        # Find the user in the database using Beanie
        admin = await Admin.find_one(Admin.email == username)
        if not admin:
            logger.info("Admin username not found in the database.")
            return None

        logger.info("Admin username exists in the database.")
        return admin
    except Exception as e:
        logger.error(f"Error while checking admin's username existence: {e}")
        return None
