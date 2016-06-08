"""
"""

# standard
import os
import string

LOWER = set(string.lowercase)
UPPER = set(string.uppercase)
DIGITS = set(string.digits)
PUNCTUATION = set(string.punctuation)
ALL = set(chr(i) for i in xrange(32, 126 + 1))

# [32,126]

def password_chars(upper=False, lower=False, digits=False, punctuation=False, custom=None):
    chars = set()
    if lower:
        chars |= LOWER
    if upper:
        chars |= UPPER
    if digits:
        chars |= DIGITS
    if punctuation:
        chars |= PUNCTUATION
    if custom:
        chars |= custom
    return chars

def remap_bytearray(bytearr, chars):
    num = len(chars)
    charmap = dict(zip(xrange(num), chars))
    return ''.join(charmap[c % num] for c in bytearr)

def generate_password(chars=ALL, length=10):
    password = bytearray(os.urandom(length))
    return remap_bytearray(password, chars)
