"""
Custom logger setup for the JANUX Authentication Gateway.

Features:
- Provides a `get_logger` function to retrieve configured loggers.
- Suppresses noisy logs from third-party libraries like FastAPI, Uvicorn, and Beanie.
- Ensures only critical or error-level logs are captured for external libraries.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging


def get_logger(name: str) -> logging.Logger:
    """
    Fetches and returns a logger with the specified name, configured
    according to the app's logging settings.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger instance.
    """
    return logging.getLogger(name)


# Suppress noisy logs from third-party libraries
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("beanie").setLevel(logging.ERROR)
