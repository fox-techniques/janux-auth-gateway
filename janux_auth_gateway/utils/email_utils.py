"""
email_utils.py

This module provides utility functions for handling email-related tasks, 
such as masking email addresses for logging and privacy protection.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import re


def mask_email(email: str) -> str:
    """
    Masks the middle characters of an email's username, keeping the first
    and last character visible while preserving the domain. If the email
    format is invalid, it returns a fully masked placeholder.

    Example:
        >>> mask_email("admin@example.com")
        'a***n@example.com'

        >>> mask_email("johndoe@gmail.com")
        'j*****e@gmail.com'

        >>> mask_email("u@b.com")
        'u@b.com'  # Short emails remain unchanged

        >>> mask_email("invalid-email")
        '***@***.***'  # Fully masked since format is invalid

    Args:
        email (str): The email address to be masked.

    Returns:
        str: The masked email address, hiding sensitive user information.
    """
    match = re.match(r"(.)(.*)(.)@(.+)", email)
    if match:
        first, middle, last, domain = match.groups()
        masked_username = first + "*" * len(middle) + last
        return f"{masked_username}@{domain}"

    # If email does not match expected format, return fully masked placeholder
    return "***@***.***"
