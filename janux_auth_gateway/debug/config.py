"""
Defines logging configurations for the JANUX Authentication Gateway.

Features:
- Dynamically detects if running in a container and adjusts log storage location.
- JSON-based structured logging for application logs.
- Plain text logging for third-party logs.
- Configures console and file handlers with customizable log levels.

Environment Variables:
- ENVIRONMENT: `local` (default) or `container` to determine log storage path.
- LOG_LEVEL: Sets the log level: DEBUG, INFO, WARNING, ERROR, or CRITICAL. (default: DEBUG).

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
import logging.config
from pythonjsonlogger import jsonlogger

# Detect environment (default: local)
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()

# Detect if running inside a container
IS_CONTAINER = ENVIRONMENT != "local"

# Define log directory based on environment
LOGS_DIR = "/var/log/janux" if IS_CONTAINER else os.path.join(os.getcwd(), "logs")


# Ensure log directory exists
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Define log file paths
LOG_FILE_PATH_APP = os.path.join(LOGS_DIR, "app.log")
LOG_FILE_PATH_ALL = os.path.join(LOGS_DIR, "all.log")

# Read the log level from the environment variable
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

# Logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(module)s %(lineno)d",
        },
        "plain": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
            "level": "INFO",
        },
        "file_app": {
            "class": "logging.FileHandler",
            "formatter": "json",
            "level": "DEBUG",
            "filename": LOG_FILE_PATH_APP,
        },
        "file_all": {
            "class": "logging.FileHandler",
            "formatter": "plain",
            "level": "DEBUG",
            "filename": LOG_FILE_PATH_ALL,
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["console", "file_app"],
            "level": "DEBUG",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": ["console", "file_all"],
            "level": "INFO",
            "propagate": False,
        },
        "pymongo": {
            "handlers": ["console", "file_all"],
            "level": "INFO",
            "propagate": False,
        },
        "third_party": {
            "handlers": ["console", "file_all"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file_app", "file_all"],
        "level": "INFO",
    },
}

# Apply logging configuration
logging.config.dictConfig(LOGGING_CONFIG)
