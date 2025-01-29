"""
Custom logger setup for the JANUX Authentication Gateway.

Features:
- Provides a `get_logger` function to retrieve configured loggers.
- Configures loggers dynamically based on environment (local vs container).
- Suppresses noisy logs from third-party libraries like FastAPI, Uvicorn, and Beanie.
- Ensures clean, readable, and organized logging for application and third-party logs.

Dependencies:
- Requires `coloredlogs` for enhanced console output.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import logging
import coloredlogs
from .config import LOGGING_CONFIG

# Apply the logging configuration
logging.config.dictConfig(LOGGING_CONFIG)

# Apply colored logs to the console handler for better readability
coloredlogs.install(
    level="INFO",
    logger=logging.getLogger("app_logger"),
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
