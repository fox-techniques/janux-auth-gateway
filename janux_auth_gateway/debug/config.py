"""
Defines logging configurations for the JANUX Authentication Gateway.

Features:
- JSON-based structured logging for better log management and integration with monitoring tools.
- Configures console and file handlers with customizable log levels.
- Automatically creates a `logs/` directory and ensures a log file exists.

Dependencies:
- Requires `python-json-logger` for JSON log formatting.

Environment Variables:
- LOG_LEVEL: Sets the log level: DEBUG, INFO, WARNING, ERROR, or CRITICAL. (default: DEBUG).

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import os
import logging.config
from pythonjsonlogger import jsonlogger

# Log file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE_PATH = os.path.join(LOGS_DIR, "app.log")

# Read the log level from the environment variable
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.FileHandler",
            "formatter": "json",
            "filename": LOG_FILE_PATH,
            "mode": "a",
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
