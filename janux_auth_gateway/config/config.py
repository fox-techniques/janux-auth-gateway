"""
config.py

Central configuration module for the application. This module loads and validates
environment variables using python-dotenv and os.

Features:
- Dynamically loads environment variables based on the specified environment.
- Provides validation for critical environment variables.
- Ensures secure handling of secrets and configuration settings.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional, List

# Determine the environment and load the appropriate .env file
env = os.getenv("ENVIRONMENT", "local")
try:
    env_file = find_dotenv(f".env.{env}")
    if not env_file:
        raise FileNotFoundError
except FileNotFoundError:
    env_file = find_dotenv(".env")

if env_file:
    load_dotenv(env_file)
else:
    raise FileNotFoundError(
        f"No suitable environment file found for {env} or default .env"
    )


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Retrieve environment variables with an optional default.

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
            "Please set it in your environment or .env file."
        )
    return value


class Config:
    """
    Configuration class to centralize and validate environment variables.
    """

    # Application configuration
    ENVIRONMENT = env
    ALLOWED_ORIGINS: List[str] = get_env_variable("ALLOWED_ORIGINS", "").split(",")
    CONTAINER = get_env_variable("CONTAINER", "False").lower() in ["true", "1"]

    # Encryption configuration
    ENCRYPTION_KEY = get_env_variable("JANUX_ENCRYPTION_KEY")
    if len(ENCRYPTION_KEY) != 44:
        raise ValueError(
            "JANUX_ENCRYPTION_KEY must be a 32-byte base64-encoded string."
        )

    # JWT configuration
    PRIVATE_KEY_PATH = get_env_variable("AUTH_PRIVATE_KEY_PATH", "private.pem")
    PUBLIC_KEY_PATH = get_env_variable("AUTH_PUBLIC_KEY_PATH", "public.pem")

    # Load private and public keys securely
    try:
        with open(PRIVATE_KEY_PATH, "r") as f:
            PRIVATE_KEY = f.read()
        with open(PUBLIC_KEY_PATH, "r") as f:
            PUBLIC_KEY = f.read()
    except FileNotFoundError:
        raise ValueError("JWT private/public key files not found.")

    # Restrict allowed algorithms
    ALGORITHM = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", "20")
    )

    # Token issuer and audience
    ISSUER = get_env_variable("ISSUER", "JANUX-server")
    AUDIENCE = get_env_variable("AUDIENCE", "JANUX-application")

    # Token URL
    USER_TOKEN_URL = get_env_variable("USER_TOKEN_URL")
    ADMIN_TOKEN_URL = get_env_variable("ADMIN_TOKEN_URL")

    # MongoDB connection URI
    MONGO_URI = get_env_variable("MONGO_URI")
    MONGO_DATABASE_NAME = get_env_variable("MONGO_DATABASE_NAME")

    # MongoDB initial admin and user credentials
    MONGO_ADMIN_EMAIL = get_env_variable("MONGO_INIT_ADMIN_EMAIL")
    MONGO_ADMIN_PASSWORD = get_env_variable("MONGO_INIT_ADMIN_PASSWORD")
    MONGO_ADMIN_FULLNAME = get_env_variable("MONGO_INIT_ADMIN_FULLNAME")
    MONGO_ADMIN_ROLE = get_env_variable("MONGO_INIT_ADMIN_ROLE", "super_admin")

    MONGO_USER_EMAIL = get_env_variable("MONGO_INIT_USER_EMAIL")
    MONGO_USER_PASSWORD = get_env_variable("MONGO_INIT_USER_PASSWORD")
    MONGO_USER_FULLNAME = get_env_variable("MONGO_INIT_USER_FULLNAME")
    MONGO_USER_ROLE = get_env_variable("MONGO_INIT_USER_ROLE", "user")

    # REDIS configuration
    REDIS_HOST = get_env_variable("REDIS_HOST", "localhost")
    REDIS_PORT = get_env_variable("REDIS_PORT", "6379")

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.

        Raises:
            ValueError: If any required environment variable is missing or invalid.
        """
        validators = {
            "PRIVATE_KEY": lambda v: isinstance(v, str) and "BEGIN PRIVATE KEY" in v,
            "PUBLIC_KEY": lambda v: isinstance(v, str) and "BEGIN PUBLIC KEY" in v,
            "MONGO_URI": lambda v: v.startswith("mongodb://")
            or v.startswith("mongodb+srv://"),
        }

        for var, validator in validators.items():
            value = getattr(Config, var, None)
            if not validator(value):
                raise ValueError(f"Invalid configuration for {var}: {value}")


# Validate configuration at import time
Config.validate()
