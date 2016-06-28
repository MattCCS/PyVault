"""
This file contains shared global variables used in the cryptographic utilities.
"""

# using AES-256
AES_KEY_BYTES = 32  # 256 bits
AES_IV_BYTES = 16  # 128 bits

NONCE_BYTES = 16  # 128 bits

DEFAULT_HASH_MODE = "sha256"
DEFAULT_ITERATIONS = int(1e5)
DERIVED_BYTES = 32  # SHA256 --> 256/8 = 32
