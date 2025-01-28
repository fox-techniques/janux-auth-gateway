"""
logging module

Provides centralized logging configuration and utilities for the JANUX Authentication Gateway.

Features:
- Centralized logging configuration using `logging.config.dictConfig`.
- Middleware for logging HTTP request details.
- Utilities for application-wide loggers.

Submodules:
- config: Defines logging configuration.
- custom_logger: Provides a `get_logger` function for accessing loggers.
- requests: Logs HTTP request details and execution times.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .custom_logger import get_logger
from .requests import log_requests

__all__ = ["get_logger", "log_requests"]
