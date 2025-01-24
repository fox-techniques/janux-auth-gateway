"""
config.py

Central configuration module for the application. This module loads and validates
environment variables using python-dotenv and os.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Configuration class to centralize and validate environment variables.
    """

    # JWT configuration
    SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
    ALGORITHM = os.getenv("AUTH_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 20))

    # MongoDB connection URI
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME")
    MONGO_SUPER_ADMIN_EMAIL = os.getenv("MONGO_SUPER_ADMIN_EMAIL")
    MONGO_SUPER_ADMIN_PASSWORD = os.getenv("MONGO_SUPER_ADMIN_PASSWORD")

    @staticmethod
    def validate():
        """
        Validates the presence of critical environment variables.
        Raises:
            ValueError: If any required environment variable is missing or invalid.
        """
        if not Config.SECRET_KEY:
            raise ValueError("Missing AUTH_SECRET_KEY environment variable.")
        if len(Config.SECRET_KEY) < 32:
            raise ValueError("AUTH_SECRET_KEY must be at least 32 characters long.")


# Validate configuration at import time
Config.validate()
