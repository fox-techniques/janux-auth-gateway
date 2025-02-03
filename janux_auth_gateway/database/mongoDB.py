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
from typing import Optional

from janux_auth_gateway.auth.passwords import verify_password, hash_password
from janux_auth_gateway.config import Config
from janux_auth_gateway.debug.custom_logger import get_logger
from janux_auth_gateway.models.user_model import User
from janux_auth_gateway.models.admin_model import Admin

# Initialize logger
logger = get_logger("auth_service_logger")


async def init_db(
    test_db=None, test_db_uri=None, test_db_name=None, test_admin=None, test_user=None
) -> None:
    """
    Initialize the MongoDB database connection with Beanie.
    Allows using a test database, custom URI, and custom database name for unit testing.

    Args:
        test_db (Optional[AsyncIOMotorDatabase]): A test database instance.
        test_db_uri (Optional[str]): The URI for the test database.
        test_db_name (Optional[str]): The name of the test database.
        test_admin (tuple): (email, password) for test admin account.
        test_user (tuple): (email, password) for test user account.

    Raises:
        SystemExit: If the MongoDB server is not reachable or authentication fails.
    """
    try:
        if test_db is not None:
            # Use test database and its values
            client = AsyncIOMotorClient(test_db_uri) if test_db_uri else test_db.client
            db = client[test_db_name] if test_db_name else test_db
        else:
            # Use production database
            client = AsyncIOMotorClient(Config.MONGO_URI)
            db = client[Config.MONGO_DATABASE_NAME]

        logger.info(f"Initializing database connection to {db.name}...")

        await init_beanie(database=db, document_models=[User, Admin])
        await db.command("ping")  # Ensure database is created

        await db["Admin"].create_index([("email", 1)], unique=True)
        await db["User"].create_index([("email", 1)], unique=True)

        logger.info(
            f"Connected to MongoDB and initialized Beanie successfully. Using database: {db.name}"
        )

        # Use test credentials if provided, otherwise fall back to Config defaults
        admin_email, admin_password, admin_fullname, admin_role = test_admin or (
            Config.MONGO_ADMIN_EMAIL,
            Config.MONGO_ADMIN_PASSWORD,
            Config.MONGO_ADMIN_FULLNAME,
            Config.MONGO_ADMIN_ROLE,
        )
        test_user_email, test_user_password, test_user_fullname, test_user_role = (
            test_user
            or (
                Config.MONGO_USER_EMAIL,
                Config.MONGO_USER_PASSWORD,
                Config.MONGO_USER_FULLNAME,
                Config.MONGO_USER_ROLE,
            )
        )

        # Ensure test users exist
        await create_admin_account(
            email=admin_email,
            password=admin_password,
            role=admin_role,
            full_name=admin_fullname,
        )
        await create_user_account(
            test_user_email,
            test_user_password,
            full_name=test_user_fullname,
            role=test_user_role,
        )

    except Exception as e:
        raise SystemExit(f"Unexpected MongoDB error: {e}")


async def create_admin_account(
    email: str,
    password: str,
    full_name: str = "Super Adminovski",
    role: str = "super_admin",
) -> None:
    """
    Creates an admin account in the database.

    Args:
        email (str): Admin's email.
        password (str): Admin's password.
        full_name (str): Admin's full name (default: "Super Adminovski").
        role (str): Admin's role (default: "super_admin").
    """
    if not email or not password:
        logger.error("Super admin email or password is missing.")
        return

    existing_admin = await Admin.find_one(Admin.email == email)

    if not existing_admin:
        admin = Admin(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        await admin.insert()
        logger.info(f"Admin account created.")
    else:
        logger.info(f"Admin account already exists.")


async def create_user_account(
    email: str,
    password: str,
    full_name: str = "Test Userovski",
    role: str = "user",
) -> None:
    """
    Creates an user account in the database.

    Args:
        email (str): Test user's email.
        password (str): Test user's password.
        full_name (str): Test user's full name (default: "Test Userovski").
        role (str): Test user's role (default: "user").
    """
    if not email or not password:
        logger.error("Test user email or password is missing.")
        return

    existing_tester = await User.find_one(User.email == email)

    if not existing_tester:
        tester = User(
            email=email,
            full_name=full_name,
            hashed_password=hash_password(password),
            role=role,
        )
        await tester.insert()
        logger.info(f"Test user account created.")
    else:
        logger.info(f"Test user account already exists.")


async def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate a user by verifying their username and password.

    Args:
        username (str): The user's email.
        password (str): The user's plain-text password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    logger.info(f"Authenticating user: {username}")

    try:
        user = await username_exists(username)
        if not user:
            logger.warning("User not found.")
            return False

        if not verify_password(password, user.hashed_password, user.email):
            logger.warning("User password verification failed.")
            return False

        logger.info("User authenticated successfully.")
        return True
    except Exception as e:
        logger.error(f"Error during user authentication: {e}")
        return False


async def authenticate_admin(username: str, password: str) -> bool:
    """
    Authenticate an admin by verifying their username and password.

    Args:
        username (str): The admin's email.
        password (str): The admin's plain-text password.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    logger.info(f"Authenticating admin: {username}")

    try:
        admin = await admin_username_exists(username)
        if not admin:
            logger.warning("Admin not found.")
            return False

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
    Check if a user exists in the database by email.

    Args:
        username (str): The user's email.

    Returns:
        Optional[User]: The user object if found, else None.
    """
    logger.info(f"Checking if user {username} exists.")
    return await User.find_one(User.email == username)


async def admin_username_exists(username: str) -> Optional[Admin]:
    """
    Check if an admin exists in the database by email.

    Args:
        username (str): The admin's email.

    Returns:
        Optional[Admin]: The admin object if found, else None.
    """
    logger.info(f"Checking if admin {username} exists.")
    return await Admin.find_one(Admin.email == username)
