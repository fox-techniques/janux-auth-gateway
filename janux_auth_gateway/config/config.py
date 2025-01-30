"""
config.py

Central configuration module for the application. This module loads and validates
environment variables using python-dotenv and os.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
from dotenv import load_dotenv, find_dotenv
from typing import Optional

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
    ALLOWED_ORIGINS = get_env_variable("ALLOWED_ORIGINS", [""])
    CONTAINER = bool(get_env_variable("CONTAINER", False))

    # JWT configuration
    SECRET_KEY = get_env_variable("AUTH_SECRET_KEY")
    ALGORITHM = get_env_variable("AUTH_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES", "20")
    )

    # Token URL
    USER_TOKEN_URL = get_env_variable("USER_TOKEN_URL")
    ADMIN_TOKEN_URL = get_env_variable("ADMIN_TOKEN_URL")

    # MongoDB connection URI
    MONGO_URI = get_env_variable("MONGO_URI")
    MONGO_DATABASE_NAME = get_env_variable("MONGO_DATABASE_NAME")
    MONGO_SUPER_ADMIN_EMAIL = get_env_variable("MONGO_SUPER_ADMIN_EMAIL")
    MONGO_SUPER_ADMIN_PASSWORD = get_env_variable("MONGO_SUPER_ADMIN_PASSWORD")
    MONGO_TESTER_EMAIL = get_env_variable("MONGO_TESTER_EMAIL")
    MONGO_TESTER_PASSWORD = get_env_variable("MONGO_TESTER_PASSWORD")

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.

        Raises:
            ValueError: If any required environment variable is missing or invalid.
        """
        validators = {
            "SECRET_KEY": lambda v: len(v) >= 32,
            "MONGO_URI": lambda v: v.startswith("mongodb://")
            or v.startswith("mongodb+srv://"),
        }

        for var, validator in validators.items():
            value = getattr(Config, var)
            if not validator(value):
                raise ValueError(f"Invalid configuration for {var}: {value}")


# Validate configuration at import time
Config.validate()
