"""
This file contains a simple API for encrypting and
decrypting data with symmetric encryption, as well as
for generating AES keys and initialization vectors.

Author:  Matthew Cotton
"""

# custom
from pykeys.crypto import errors
from pykeys.crypto import settings
from pykeys.crypto import generic_utils
from pykeys.crypto import integrity_utils
from pykeys.crypto import packing_utils

# installed
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_hmac(aes_key, plaintext):
    """Returns packed_ciphertext."""
    aes_iv = generic_utils.iv()
    ciphertext = encrypt(aes_key, aes_iv, plaintext)
    hmac_sig = integrity_utils.hmac_generate(aes_key, plaintext)
    return packing_utils.pack(aes_iv, ciphertext, hmac_sig)


def decrypt_hmac(aes_key, packed_ciphertext):
    """Returns plaintext."""
    (aes_iv, ciphertext, hmac_sig) = packing_utils.unpack(packed_ciphertext)
    plaintext = decrypt(aes_key, aes_iv, ciphertext)
    if not integrity_utils.hmac_verify(aes_key, plaintext, hmac_sig):
        raise errors.SignatureVerificationFailedError()
    return plaintext

####################################


def generate_key_and_iv(key_length=settings.AES_KEY_BYTES, iv_length=settings.AES_IV_BYTES):
    """
    Generates a random AES key and initialization vector
    using the os.urandom method (recommended for cryptographic use).

    The key and IV length are determined by the settings file.

    + produces AES key and IV (private!)
    """
    aes_key = generic_utils.nonce(key_length)
    aes_iv = generic_utils.nonce(iv_length)

    return (aes_key, aes_iv)


def encrypt(aes_key, aes_iv, plaintext):
    """
    Encrypts the given plaintext with the given
    key and initialization vector using
    AES-256 in Counter (CTR) mode.

    + produces ciphertext (public)
    """
    assert type(plaintext) is bytes

    backend = default_backend()

    try:
        # AES-256 in CTR mode
        cipher = Cipher(algorithms.AES(aes_key), modes.CTR(aes_iv), backend=backend)
        encryptor = cipher.encryptor()

        return encryptor.update(plaintext) + encryptor.finalize()

    except ValueError as err:
        raise errors.SymmetricEncryptionException(err)


def decrypt(aes_key, aes_iv, ciphertext):
    """
    Decrypts the given ciphertext with the given
    key and initialization vector using
    AES-256 in Counter (CTR) mode.

    + produces plaintext (private!)
    """
    backend = default_backend()

    try:
        # AES-256 in CTR mode
        cipher = Cipher(algorithms.AES(aes_key), modes.CTR(aes_iv), backend=backend)
        decryptor = cipher.decryptor()

        return decryptor.update(ciphertext)

    except ValueError as err:
        raise errors.SymmetricEncryptionException(err)
