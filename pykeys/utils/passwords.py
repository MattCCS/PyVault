"""
"""

# standard
import os
import string

LOWER = set(string.lowercase)
UPPER = set(string.uppercase)
DIGITS = set(string.digits)
SPECIAL = set(string.punctuation)
ALL = set(chr(i) for i in xrange(32, 126 + 1))

# [32,126]

def password_chars(upper=False, lower=False, digits=False, special=False, custom=None):
    chars = set()
    if lower:
        chars |= LOWER
    if upper:
        chars |= UPPER
    if digits:
        chars |= DIGITS
    if special:
        chars |= SPECIAL
    if custom:
        chars |= custom
    return chars

def generate_password(chars=ALL, length=10):
    password = bytearray(os.urandom(length))

    num = len(chars)

    charmap = dict(zip(xrange(num), chars))

    return ''.join(charmap[c % num] for c in password)
