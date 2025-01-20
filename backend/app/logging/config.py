"""
- Formatters: Define the format of log messages. The detailed formatter is used for file logging to include more information.
- Handlers: Determine where log messages go. Messages can be printed to the console and written to a file app.log.
- Loggers: The app_logger is a custom logger configured to use both handlers. The root logger is also configured to ensure that any logging messages not caught by app_logger are still handled appropriately.
- Propagation: Setting propagate to False for app_logger prevents log messages from being handled by the root logger’s handlers again, avoiding duplicate logging.
"""

import os

# Calculate the absolute path to the logs directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LOG_FILE_PATH = os.path.join(LOGS_DIR, "app.log")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] in %(module)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": LOG_FILE_PATH,
            "mode": "a",
        },
    },
    "loggers": {
        "app_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}
