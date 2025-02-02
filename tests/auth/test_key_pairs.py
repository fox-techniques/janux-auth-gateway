"""
test_keys.py

Unit tests for cryptographic key generation in the JANUX Authentication Gateway.

Tests:
- RSA, Ed25519, and ECDSA key pair generation.
- AES-GCM encryption of private keys.
- Handling of invalid key sizes, curves, and key types.
- Proper validation of encryption key.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

import pytest
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, ed25519, ec
from janux_auth_gateway.auth.key_pairs import (
    generate_rsa_key_pair,
    generate_ed25519_key_pair,
    generate_ecdsa_key_pair,
    generate_key_pair,
    encrypt_private_key,
    CIPHER_KEY,
)


@pytest.fixture(scope="function")
def mock_cipher_key(mocker):
    """
    Fixture to mock the encryption key used in Fernet encryption.
    Ensures encryption key is valid and 44 characters long.
    """
    valid_key = base64.urlsafe_b64encode(os.urandom(32)).decode()
    mocker.patch("janux_auth_gateway.auth.key_pairs.CIPHER_KEY", valid_key)
    mocker.patch("janux_auth_gateway.auth.key_pairs.cipher", Fernet(valid_key.encode()))


def test_encrypt_private_key(mock_cipher_key):
    """
    Test that private keys are correctly encrypted using AES-GCM.

    Expected Outcome:
    - The output should be a valid encrypted string.
    - The length should be greater than the original.
    """
    private_key_pem = b"FAKE_PRIVATE_KEY"
    encrypted_key = encrypt_private_key(private_key_pem)

    assert isinstance(encrypted_key, bytes)
    assert len(encrypted_key) > len(private_key_pem)


@pytest.mark.parametrize("key_size", [2048, 4096])
def test_generate_rsa_key_pair(key_size, mock_cipher_key):
    """
    Test RSA key pair generation.

    Expected Outcome:
    - Generates an RSA key pair with the given key size.
    - Private key should be encrypted.
    """
    encrypted_private_key, public_key = generate_rsa_key_pair(key_size)

    assert isinstance(encrypted_private_key, bytes)
    assert isinstance(public_key, bytes)
    assert b"-----BEGIN PUBLIC KEY-----" in public_key


def test_generate_rsa_key_pair_invalid_size(mock_cipher_key):
    """
    Test RSA key generation with an invalid key size.

    Expected Outcome:
    - Should raise ValueError when key size is below 2048 bits.
    """
    with pytest.raises(ValueError, match="RSA key size must be at least 2048 bits."):
        generate_rsa_key_pair(1024)


def test_generate_ed25519_key_pair(mock_cipher_key):
    """
    Test Ed25519 key pair generation.

    Expected Outcome:
    - Generates an Ed25519 key pair.
    - Private key should be encrypted.
    """
    encrypted_private_key, public_key = generate_ed25519_key_pair()

    assert isinstance(encrypted_private_key, bytes)
    assert isinstance(public_key, bytes)
    assert b"-----BEGIN PUBLIC KEY-----" in public_key


@pytest.mark.parametrize("curve", ["P-256", "P-384", "P-521"])
def test_generate_ecdsa_key_pair(curve, mock_cipher_key):
    """
    Test ECDSA key pair generation.

    Expected Outcome:
    - Generates an ECDSA key pair using the specified curve.
    - Private key should be encrypted.
    """
    encrypted_private_key, public_key = generate_ecdsa_key_pair(curve)

    assert isinstance(encrypted_private_key, bytes)
    assert isinstance(public_key, bytes)
    assert b"-----BEGIN PUBLIC KEY-----" in public_key


def test_generate_ecdsa_key_pair_invalid_curve(mock_cipher_key):
    """
    Test ECDSA key generation with an invalid curve.

    Expected Outcome:
    - Should raise ValueError when using an unsupported curve.
    """
    with pytest.raises(
        ValueError, match="Invalid curve choice. Use 'P-256', 'P-384', or 'P-521'."
    ):
        generate_ecdsa_key_pair("P-123")


@pytest.mark.parametrize(
    "key_type,kwargs",
    [
        ("rsa", {"key_size": 2048}),
        ("ed25519", {}),
        ("ecdsa", {"curve": "P-256"}),
    ],
)
def test_generate_key_pair_valid_types(key_type, kwargs, mock_cipher_key):
    """
    Test the dynamic key generation function.

    Expected Outcome:
    - Generates the correct type of key pair based on input parameters.
    """
    encrypted_private_key, public_key = generate_key_pair(key_type, **kwargs)

    assert isinstance(encrypted_private_key, bytes)
    assert isinstance(public_key, bytes)
    assert b"-----BEGIN PUBLIC KEY-----" in public_key


def test_generate_key_pair_invalid_type(mock_cipher_key):
    """
    Test generate_key_pair function with an invalid key type.

    Expected Outcome:
    - Should raise ValueError for unsupported key types.
    """
    with pytest.raises(
        ValueError, match="Invalid key type. Choose 'rsa', 'ed25519', or 'ecdsa'."
    ):
        generate_key_pair("invalid_key_type")


def test_cipher_key_length_validation():
    """
    Test that the encryption key validation enforces the correct length.

    Expected Outcome:
    - If `JANUX_ENCRYPTION_KEY` is not 44 characters, a ValueError is raised.
    """
    with pytest.raises(
        ValueError,
        match="JANUX_ENCRYPTION_KEY must be a 32-byte base64-encoded string.",
    ):
        os.environ["JANUX_ENCRYPTION_KEY"] = "invalid_key"
        import importlib
        import janux_auth_gateway.auth.key_pairs

        importlib.reload(janux_auth_gateway.auth.key_pairs)
