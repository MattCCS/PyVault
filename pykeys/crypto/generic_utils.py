"""
"""

# standard
import os

# custom
from pykeys.crypto import settings


def nonce(n=settings.NONCE_BYTES):
    return os.urandom(n)


def iv(n=settings.AES_IV_BYTES):
    return nonce(n)
