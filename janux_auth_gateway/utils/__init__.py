"""
utils package

This package contains utility functions used across the JANUX Authentication Gateway,
such as email masking, string formatting, and data validation.

Modules:
    - email_utils: Utility functions for handling email-related operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .email_utils import mask_email

__all__ = ["mask_email"]
