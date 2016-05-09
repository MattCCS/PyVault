#!/usr/local/bin/python
#
# /\ THIS IS CRUCIAL!!! SPEEDS UP HASHING IMMENSELY!!!
#
# Copyright 2014 Matthew Cotton

####################################
# Standard Library
import hashlib
import getpass
import string
import sys
import os

####################################
# Custom
import utils

DEFAULT_ITERATIONS  = 100000
DEFAULT_SALT_LENGTH = 16
DEFAULT_PW_LENGTH   = 16

ALPHANUM_AND_DIGITS = string.lowercase + string.uppercase + string.digits

_TRUE_STDOUT = sys.stdout # preserve the true value of sys.stdout for later
sys.stdout = sys.stderr # sys.stdout is now pointing to sys.stderr! woohoo!

# PEPPER = utils.unhexed('a08a99b9b57baf9b2b05480bceca7c2b867e798983f3c82bcc3139fc602d1ca5') # pre-generated with os.urandom


###############
# modes (ASCII):
#
# 0 - alphanumeric                      (62)
# 1 - alphanumeric,!,?                  (64 -- even divisor 256)
# 2 - all basic printable characters    (95)
# 3 - ASCII first 128 (+ CONTROL CHARS) (128 -- even divisor 256)
# 4 - printable, some extended          (128 -- even divisor 256)
# 5 - ALL ASCII characters              (256 -- MAX)
#
# new:
# 6 - hex, lowercase                    (16 -- even divisor 256)
# 7 - hex, uppercase                    (16 -- even divisor 256)

ASCII_ALPHANUM                  = range(48,58) + range(65,91) + range(97,123)
ASCII_ALPHANUM_EXCL_QU_64       = ASCII_ALPHANUM + [33, 63]
ASCII_PRINTABLE                 = range(32,127)
ASCII_FIRST_128                 = range(0,128)
ASCII_PRINTABLE_EXTEND_128      = ASCII_PRINTABLE + range(128,161)
ASCII_ALL_256                   = range(0,256)
HEX_LOWER_16                    = range(48,58) + range(97,97+6)
HEX_UPPER_16                    = range(48,58) + range(65,65+6)

MODES = [
    ASCII_ALPHANUM, 
    ASCII_ALPHANUM_EXCL_QU_64, 
    ASCII_PRINTABLE, 
    ASCII_FIRST_128, 
    ASCII_PRINTABLE_EXTEND_128, 
    ASCII_ALL_256,
    HEX_LOWER_16,
    HEX_UPPER_16,
]

assert len(ASCII_ALPHANUM_EXCL_QU_64) == 64
assert len(ASCII_PRINTABLE_EXTEND_128) == 128


def normalize(vals, mode):
    return map(lambda n: mode[n % len(mode)], vals)

def chr_ord_convert(it, to_nums):
    return map(ord, it) if to_nums else ''.join(chr(c) for c in it)

def remap_string(s, char_set):
    assert len(char_set) <= 256

    if len(char_set) == 256:
        return s
    else:
        vals = chr_ord_convert(s, True)
        vals = normalize(vals, char_set)
        return chr_ord_convert(vals, False)

def sanity_check_chars(chars):
    if not chars:
        raise RuntimeError("No characters provided!")

    assert len(chars) >= 62 # must at least allow alphanum + digits
    assert len(chars) <= 256 # guarantee len(chars) <= max allowable
    assert len(set(chars)) == len(chars) # no internal duplicates

def get_input(prompt='', echo=True):
    if echo:
        sys.stderr.write(prompt)
        sys.stderr.flush()
        return raw_input()
    else:
        return getpass.getpass(prompt)

def gen_salt(n=DEFAULT_SALT_LENGTH):
    return os.urandom(n)

def myhash(secret, salt, iterations, length, chars=MODES[2], b16=False):

    if type(chars) == str:
        chars = map(ord, chars)

    ####################################
    # guarantee valid character set
    sanity_check_chars(chars)

    assert len(secret) >= 16 # at least 128 bits
    assert len(salt)   >= DEFAULT_SALT_LENGTH # at least 128 bits

    assert length >= 8 # please, jesus.
    assert length <= 512/8 # max effective length for sha512

    result = remap_string(hashlib.pbkdf2_hmac("sha512", secret, salt, iterations, length), chars)

    # COPYABLE TO CLIPBOARD !!!
    # _TRUE_STDOUT.write(result)
    # _TRUE_STDOUT.flush()

    return result if not b16 else utils.hexed(result)

def simple_hash(secret, salt, iterations, length, chars=None):
    if chars is not None:
        chars = chr_ord_convert(chars, to_nums=True)
    else:
        chars = MODES[2]
    return myhash(secret, salt, iterations, length, chars=chars)

print myhash('once_upon_a_time', 'sfkjgfsghfsjkgjsfgjkf', 200000, 24, b16=0)





