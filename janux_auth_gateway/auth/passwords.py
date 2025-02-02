"""
passwords.py

Utility module for password hashing and verification using bcrypt and argon2.
This module leverages Passlib's CryptContext to provide secure password management.

Features:
- Hash passwords securely using Argon2 and bcrypt.
- Verify plain passwords against hashed passwords.
- Ensures input validation to prevent misuse.
- Upgrades outdated password hashes to the latest standard.
- Enforces password complexity requirements.
- Implements rate-limiting for password verification to prevent brute-force attacks.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import re
import redis
from passlib.context import CryptContext
from fastapi import HTTPException
from janux_auth_gateway.config import Config
from janux_auth_gateway.debug.custom_logger import get_logger

# Initialize logger
logger = get_logger("auth_service_logger")


redis_instance = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)

# Configure the password hashing context with Argon2 and bcrypt
bcrypt_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


def is_password_secure(password: str) -> bool:
    """
    Checks if a password meets security requirements.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password meets complexity requirements, False otherwise.
    """


def is_password_secure(password: str) -> bool:
    """
    Checks if a password meets security requirements.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password meets complexity requirements, False otherwise.
    """
    return (
        len(password) >= 8
        and bool(re.search(r"[A-Z]", password))
        and bool(re.search(r"[a-z]", password))
        and bool(re.search(r"[0-9]", password))
        and bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))
    )


def hash_password(password: str) -> str:
    """
    Hashes the given password securely using Argon2 or bcrypt.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: The securely hashed password.

    Raises:
        ValueError: If the password is empty, not a string, or too weak.
    """
    logger.info("Hashing password...")

    if not isinstance(password, str):
        logger.error("Password must be a string.")
        raise ValueError("Password must be a string.")

    password = password.strip()
    if not password:
        logger.error("Password cannot be empty.")
        raise ValueError("Password cannot be empty.")

    if not is_password_secure(password):
        logger.error("Password does not meet security requirements.")
        raise ValueError(
            "Password must be at least 8 characters long, include uppercase, lowercase, a number, and a special character."
        )

    return bcrypt_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
    user_identifier: str,
    redis_client=redis_instance,
) -> bool:
    """
    Verifies a plain-text password against a securely hashed password and implements rate-limiting.

    Args:
        plain_password (str): The plain-text password to verify.
        hashed_password (str): The hashed password stored in the database.
        user_identifier (str): A unique identifier for the user (email or ID).
        redis_client (redis.Redis): The Redis client for rate-limiting. Defaults to real Redis instance.

    Returns:
        bool: True if the password matches, False otherwise.

    Raises:
        ValueError: If either input is not a string or is empty.
        HTTPException: If too many failed login attempts occur.
    """
    logger.info(f"Verifying password for user: {user_identifier}")

    if not isinstance(plain_password, str) or not isinstance(hashed_password, str):
        logger.error("Both plain and hashed passwords must be strings.")
        raise ValueError("Both passwords must be strings.")

    plain_password = plain_password.strip()
    hashed_password = hashed_password.strip()

    if not plain_password or not hashed_password:
        logger.error("Passwords cannot be empty.")
        raise ValueError("Passwords cannot be empty.")

    attempts_key = f"login_attempts:{user_identifier}"
    attempts = redis_client.get(attempts_key)

    if attempts and int(attempts) >= 5:
        logger.warning(f"Too many login attempts for user: {user_identifier}")
        raise HTTPException(
            status_code=429, detail="Too many login attempts. Please try again later."
        )

    try:
        if bcrypt_context.verify(plain_password, hashed_password):
            redis_client.delete(attempts_key)  # Reset attempts on success
            return True
        else:
            redis_client.incr(attempts_key)
            redis_client.expire(attempts_key, 900)  # Expire in 15 minutes
            return False
    except Exception as e:
        logger.error(f"Error during password verification: {e}")
        return False


def upgrade_password_hash(password: str, hashed_password: str) -> str:
    """
    Upgrades an old password hash to the latest hashing scheme if needed.

    Args:
        password (str): The plain-text password.
        hashed_password (str): The existing hashed password.

    Returns:
        str: The updated password hash (if rehashed) or the original hash if already secure.
    """
    if bcrypt_context.needs_update(hashed_password):
        logger.info("Upgrading password hash to the latest security standard.")
        return hash_password(password)
    return hashed_password
