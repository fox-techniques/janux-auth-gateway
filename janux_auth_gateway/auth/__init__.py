"""
auth module

Handles authentication features for the JANUX Authentication Gateway.

Submodules:
- jwt: Manages JSON Web Tokens (JWTs) for secure authentication.
- passwords: Provides utilities for password hashing and verification.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from .jwt import create_access_token, get_current_user, get_current_admin
from .passwords import hash_password, verify_password
from .key_pairs import (
    generate_rsa_key_pair,
    generate_ed25519_key_pair,
    generate_ecdsa_key_pair,
    generate_key_pair,
)

__all__ = [
    "create_access_token",
    "get_current_user",
    "get_current_admin",
    "hash_password",
    "verify_password",
    "generate_rsa_key_pair",
    "generate_ed25519_key_pair",
    "generate_ecdsa_key_pair",
    "generate_key_pair",
]
