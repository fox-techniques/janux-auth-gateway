"""
keys.py

This module provides functionality to generate cryptographic key pairs for users in the JANUX Authentication Gateway.
Supported key types include:
- RSA (2048-bit & 4096-bit): Widely supported, good for encryption/signing.
- Ed25519: Modern, fast, and secure, commonly used for authentication and signing.
- ECDSA (P-256, P-384, P-521): Smaller keys with strong security, suitable for digital signatures.

Private keys are securely encrypted before storage using AES-GCM encryption.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from cryptography.hazmat.primitives.asymmetric import rsa, ed25519, ec
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet
from typing import Tuple
import os

# Generate a secret key for AES encryption (should be stored securely, e.g., in an env variable)
CIPHER_KEY = os.getenv("JANUX_ENCRYPTION_KEY", Fernet.generate_key().decode())

# Validate encryption key length (must be 32 bytes base64-encoded, which is 44 characters)
if len(CIPHER_KEY) != 44:
    raise ValueError("JANUX_ENCRYPTION_KEY must be a 32-byte base64-encoded string.")

cipher = Fernet(CIPHER_KEY.encode())


def encrypt_private_key(private_key_pem: bytes) -> bytes:
    """
    Encrypts the private key using AES-GCM.

    Args:
        private_key_pem (bytes): The private key in PEM format.

    Returns:
        bytes: The encrypted private key.
    """
    return cipher.encrypt(private_key_pem)


def generate_rsa_key_pair(key_size: int = 2048) -> Tuple[bytes, bytes]:
    """
    Generates an RSA public-private key pair.

    Args:
        key_size (int): Key size, default is 2048. Must be at least 2048 bits.

    Returns:
        Tuple[bytes, bytes]: (encrypted_private_key_pem, public_key_pem)
    """
    if key_size < 2048:
        raise ValueError("RSA key size must be at least 2048 bits.")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return encrypt_private_key(private_key_pem), public_key_pem


def generate_ed25519_key_pair() -> Tuple[bytes, bytes]:
    """
    Generates an Ed25519 public-private key pair.

    Returns:
        Tuple[bytes, bytes]: (encrypted_private_key_pem, public_key_pem)
    """
    private_key = ed25519.Ed25519PrivateKey.generate()

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return encrypt_private_key(private_key_pem), public_key_pem


def generate_ecdsa_key_pair(curve: str = "P-256") -> Tuple[bytes, bytes]:
    """
    Generates an ECDSA public-private key pair.

    Args:
        curve (str): Elliptic curve to use. Options: "P-256", "P-384", "P-521".

    Returns:
        Tuple[bytes, bytes]: (encrypted_private_key_pem, public_key_pem)
    """
    curve_options = {
        "P-256": ec.SECP256R1(),
        "P-384": ec.SECP384R1(),
        "P-521": ec.SECP521R1(),
    }

    if curve not in curve_options:
        raise ValueError("Invalid curve choice. Use 'P-256', 'P-384', or 'P-521'.")

    private_key = ec.generate_private_key(curve_options[curve])

    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_key_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return encrypt_private_key(private_key_pem), public_key_pem


# Mapping function names for dynamic key generation
KEY_GENERATORS = {
    "rsa": generate_rsa_key_pair,
    "ed25519": generate_ed25519_key_pair,
    "ecdsa": generate_ecdsa_key_pair,
}


def generate_key_pair(key_type: str, **kwargs) -> Tuple[bytes, bytes]:
    """
    Generate a key pair based on user preference.

    Args:
        key_type (str): Type of key pair to generate. Options: "rsa", "ed25519", "ecdsa".
        **kwargs: Additional arguments for key generation (e.g., key_size for RSA, curve for ECDSA).

    Returns:
        Tuple[bytes, bytes]: (encrypted_private_key_pem, public_key_pem)
    """
    if key_type not in KEY_GENERATORS:
        raise ValueError("Invalid key type. Choose 'rsa', 'ed25519', or 'ecdsa'.")

    return KEY_GENERATORS[key_type](**kwargs)
