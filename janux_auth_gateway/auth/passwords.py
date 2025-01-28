"""
passwords.py

Utility module for password hashing and verification using bcrypt. This module
leverages Passlib's CryptContext to provide secure password management.

Features:
- Hash passwords securely using bcrypt.
- Verify plain passwords against hashed passwords.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from passlib.context import CryptContext
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")

# Configure the password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash the given password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The securely hashed password.

    Raises:
        ValueError: If the password is not a string or is empty.
    """
    logger.info("Hashing password...")

    if not isinstance(password, str):
        logger.error("Password must be a string.")
        raise ValueError("Password must be a string.")

    if not password.strip():
        logger.error("Password cannot be empty.")
        raise ValueError("Password cannot be empty.")

    return bcrypt_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The previously hashed password for comparison.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    logger.info("Verifying password against hashed password...")

    try:
        if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
            logger.error("Both plain and hashed passwords must be strings.")
            return False

        if not plain_password.strip() or not hashed_password.strip():
            logger.error("Passwords cannot be empty.")
            return False

        return bcrypt_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Error during password verification: {e}")
        return False
