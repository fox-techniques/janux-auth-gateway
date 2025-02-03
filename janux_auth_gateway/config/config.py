"""
config.py

Central configuration module for the JANUX Authentication Gateway.

Features:
- Dynamically loads environment variables based on the specified environment.
- Provides validation for critical environment variables.
- Ensures secure handling of secrets and configuration settings.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
import glob

from typing import Optional, List


def read_secret(secret_name):
    """
    Reads secrets from:
    1. `/run/secrets/` (Docker Secrets in Production)
    2. `./secrets/` (Local Development on Host)
    3. Falls back to environment variables if both locations fail.
    """
    secret_paths = [
        f"/run/secrets/{secret_name}",  # Docker/Kubernetes Secrets (Production)
        f"./secrets/{secret_name}",  # Local Development (Host System)
    ]

    for path in secret_paths:
        if os.path.exists(path):
            with open(path, "r") as file:
                return file.read().strip()

    return os.getenv(secret_name)  # Fallback to environment variable


def read_jwt_key(key_type: str) -> str:
    """
    Reads a private or public key from the appropriate secret storage location.

    - Looks for `private*.pem` or `public*.pem` in `/run/secrets/` (Docker)
    - Falls back to `./secrets/` (Local Development)

    Args:
        key_type (str): Either "private" or "public".

    Returns:
        str: The key content as a string.

    Raises:
        ValueError: If no key file is found.
    """
    if key_type not in ["private", "public"]:
        raise ValueError("Invalid key_type. Must be 'private' or 'public'.")

    # Define search patterns
    key_pattern = f"{key_type}*.pem"

    # Define search locations
    search_paths = [
        "/run/secrets/",  # Docker/K8s Secrets (Production)
        "./secrets/",  # Local Development (Project Root)
    ]

    # Look for a matching key file in the search locations
    for path in search_paths:
        matching_files = glob.glob(os.path.join(path, key_pattern))
        if matching_files:
            key_file = matching_files[0]  # Use the first matching file
            with open(key_file, "r") as file:
                return file.read().strip()

    raise ValueError(f"No {key_type} key file found in {search_paths}")


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Retrieve non-sensitive environment variables with an optional default.

    Args:
        var_name (str): The name of the environment variable to retrieve.
        default (Optional[str]): The default value if the variable is not set.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set and no default is provided.
    """
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(
            f"Missing environment variable: '{var_name}'. "
            "Please set it in your environment."
        )
    return value


class Config:
    """
    Configuration class for JANUX Authentication Gateway.
    Loads environment variables and secrets securely.
    """

    # Application settings
    ENVIRONMENT = get_env_variable("ENVIRONMENT", "local")
    ALLOWED_ORIGINS: List[str] = get_env_variable("ALLOWED_ORIGINS", "*").split(",")

    # 🔐 Encryption Key (AES)
    JANUX_ENCRYPTION_KEY = read_secret("janux_encryption_key".upper())

    # 🔑 JWT Authentication Keys
    JWT_PRIVATE_KEY = read_jwt_key(key_type="private")
    JWT_PUBLIC_KEY = read_jwt_key(key_type="public")

    JWT_ALGORITHM = "RS256"

    # 🔥 JWT Token Settings
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", "20")
    )
    TOKEN_ISSUER = get_env_variable("TOKEN_ISSUER", "JANUX-server")
    TOKEN_AUDIENCE = get_env_variable("TOKEN_AUDIENCE", "JANUX-application")

    # 🗝️ Token Endpoints
    USER_TOKEN_URL = get_env_variable("USER_TOKEN_URL", "/auth/login")
    ADMIN_TOKEN_URL = get_env_variable("ADMIN_TOKEN_URL", "/auth/login")

    # 🛢️ Database (MongoDB)
    MONGO_URI = read_secret("mongo_uri".upper())
    MONGO_DATABASE_NAME = get_env_variable("MONGO_DATABASE_NAME", "users_db")

    # 👤 MongoDB Initial Admin Credentials
    MONGO_ADMIN_EMAIL = read_secret("mongo_admin_email".upper())
    MONGO_ADMIN_PASSWORD = read_secret("mongo_admin_password".upper())
    MONGO_ADMIN_FULLNAME = read_secret("mongo_admin_fullname".upper())
    MONGO_ADMIN_ROLE = read_secret("mongo_admin_role".upper())

    # 👤 MongoDB Initial User Credentials
    MONGO_USER_EMAIL = read_secret("mongo_user_email".upper())
    MONGO_USER_PASSWORD = read_secret("mongo_user_password".upper())
    MONGO_USER_FULLNAME = read_secret("mongo_user_fullname".upper())
    MONGO_USER_ROLE = read_secret("mongo_user_role".upper())

    # 🔄 Redis Configuration
    REDIS_HOST = get_env_variable("REDIS_HOST", "localhost")
    REDIS_PORT = int(get_env_variable("REDIS_PORT", "6379"))

    @staticmethod
    def validate():
        """
        Ensures critical secrets are available and valid.
        Raises an error if required values are missing.
        """
        if not Config.JANUX_ENCRYPTION_KEY:
            raise ValueError("Missing `janux_encryption_key` for encryption.")
        if (
            not Config.JWT_PRIVATE_KEY
            or "BEGIN PRIVATE KEY" not in Config.JWT_PRIVATE_KEY
        ):
            raise ValueError("Invalid or missing `jwt_private_key` for signing JWTs.")
        if not Config.JWT_PUBLIC_KEY or "BEGIN PUBLIC KEY" not in Config.JWT_PUBLIC_KEY:
            raise ValueError("Invalid or missing `jwt_public_key` for verifying JWTs.")
        if not Config.MONGO_URI:
            raise ValueError("Missing `mongo_uri` for database connection.")
        if not Config.MONGO_ADMIN_PASSWORD:
            raise ValueError("Missing `mongo_admin_password`.")
        if not Config.MONGO_USER_PASSWORD:
            raise ValueError("Missing `mongo_user_password`.")


# Validate configuration on startup
Config.validate()
