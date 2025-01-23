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
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("app_logger")

# Configure the password hashing context
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash the given password using bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The securely hashed password.
    """
    logger.info("Hashing password...")
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
    return bcrypt_context.verify(plain_password, hashed_password)
