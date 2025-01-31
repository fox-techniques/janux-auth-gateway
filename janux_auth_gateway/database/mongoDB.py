"""
mongoDB.py

This module handles MongoDB connections and user authentication operations using Beanie ODM.

Features:
- Connect to MongoDB using a configurable URI.
- Authenticate users and admins by verifying their credentials securely.
- Ensure default admin and tester accounts exist for testing and administration.
- Implements logging for all critical operations.
- Uses unique indexing for user and admin email fields to enforce uniqueness.

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


async def init_db(test_db=None) -> None:
    """
    Initialize the MongoDB database connection with Beanie.
    Allows using a test database for unit testing.

    Args:
        test_db (Optional[AsyncIOMotorClient]): A test database instance.

    Raises:
        SystemExit: If the MongoDB server is not reachable or authentication fails.
    """
    try:
        client = test_db or AsyncIOMotorClient(Config.MONGO_URI)
        db = client[Config.MONGO_DATABASE_NAME]

        logger.info("Initializing database connection...")
        await init_beanie(database=db, document_models=[User, Admin])

        logger.info("Connected to MongoDB and initialized Beanie successfully.")

    except ServerSelectionTimeoutError:
        raise SystemExit("MongoDB connection timeout.")
    except OperationFailure:
        raise SystemExit("MongoDB authentication failed.")
    except Exception as general_error:
        raise SystemExit(f"Unexpected MongoDB error: {general_error}")


async def ensure_super_admin_exists() -> None:
    """
    Ensures a super admin account exists in the database. Creates one if it doesn't.
    """
    admin_email = Config.MONGO_SUPER_ADMIN_EMAIL
    admin_password = Config.MONGO_SUPER_ADMIN_PASSWORD

    if not admin_email or not admin_password:
        logger.error("Super admin email or password is not configured.")
        return

    if not await Admin.find_one(Admin.email == admin_email):
        admin = Admin(
            email=admin_email,
            full_name="Super Admin",
            hashed_password=hash_password(admin_password),
            role="super_admin",
        )
        await admin.insert()
        logger.info(f"Default admin account created: {admin_email}")


async def ensure_tester_exists() -> None:
    """
    Ensures a tester account exists in the database. Creates one if it doesn't.
    """
    tester_email = Config.MONGO_TESTER_EMAIL
    tester_password = Config.MONGO_TESTER_PASSWORD

    if not await User.find_one(User.email == tester_email):
        tester = User(
            email=tester_email,
            full_name="Tester",
            hashed_password=hash_password(tester_password),
            role="tester",
        )
        await tester.insert()
        logger.info(f"Default tester account created: {tester_email}")


async def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying their username and password.

    Args:
        username (str): The user's email.
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

        # Fix: Pass `user.email` as the `user_identifier`
        if not verify_password(password, user.hashed_password, user.email):
            logger.warning("Password verification failed.")
            return False

        logger.info("User authenticated successfully.")
        return True
    except Exception as e:
        logger.error(f"Error during user authentication: {e}")
        return False


async def authenticate_admin(username: str, password: str) -> bool:
    """
    Authenticate an admin  by verifying their username and password.

    Args:
        username (str): The admin's email.
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

        # Fix: Pass `user.email` as the `user_identifier`
        if not verify_password(password, admin.hashed_password, admin.email):
            logger.warning("Admin password verification failed.")
            return False

        logger.info("Admin authenticated successfully.")
        return True
    except Exception as e:
        logger.error(f"Error during admin authentication: {e}")
        return False


async def username_exists(username: str) -> Optional[User]:
    """
    Checks if a username exists in the database.
    """
    return await User.find_one(User.email == username)


async def admin_username_exists(username: str) -> Optional[Admin]:
    """
    Checks if an admin's username exists in the database.
    """
    return await Admin.find_one(Admin.email == username)
