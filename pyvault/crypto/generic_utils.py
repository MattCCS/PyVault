"""
"""

# standard
import os

# custom
from pyvault.crypto import crypto_settings


def nonce(n=crypto_settings.NONCE_BYTES):
    return os.urandom(n)


def iv(n=crypto_settings.AES_IV_BYTES):
    return nonce(n)
