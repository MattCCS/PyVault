"""
This file contains functions for generating and verifying HMACs.
"""

# standard
import hashlib
import hmac


def hmac_generate(key, plaintext):
    """
    Generates an HMAC for the plaintext with the key.
    """
    h = hmac.new(key, msg=plaintext, digestmod=hashlib.sha256)
    h.update(plaintext)
    return h.digest()


def hmac_verify(key, plaintext, signature):
    """
    Generates the HMAC for the plaintext with the key against the signature.
    """
    h = hmac.new(key, msg=plaintext, digestmod=hashlib.sha256)
    h.update(plaintext)
    return h.digest() == signature
