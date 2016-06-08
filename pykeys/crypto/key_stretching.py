
# standard
import hashlib

# custom
from pykeys.crypto import settings


def stretch(key, salt, mode=settings.DEFAULT_HASH_MODE, iterations=settings.DEFAULT_ITERATIONS, length=settings.DERIVED_BYTES):
    """
    Returns:
    1) derived key, and
    2) (mode, salt, iterations, length), which can be ignored
    """
    mode = str(mode)  # required by stdlib
    derived_key = hashlib.pbkdf2_hmac(mode, key, salt, iterations, length)
    key_stretching_data = (mode, salt, iterations, length)
    return (derived_key, key_stretching_data)
