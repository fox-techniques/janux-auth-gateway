"""
custom_logger.py

Provides a centralized logger configuration for the application.

Features:
- Applies logging configuration using the Python `logging` module.
- Exposes a helper function to retrieve configured logger instances.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
from .config import LOGGING_CONFIG

# Apply the logging configuration globally
logging.config.dictConfig(LOGGING_CONFIG)


def get_logger(name: str) -> logging.Logger:
    """
    Fetches and returns a logger with the specified name, configured according to the app's logging settings.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger instance.
    """
    return logging.getLogger(name)
