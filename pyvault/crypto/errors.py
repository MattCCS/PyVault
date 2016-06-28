"""
This file contains custom exception classes used for
differentiating expected and unexpected cryptographic exceptions.
"""

####################################

# password errors
class PasswordHashComparisonError (Exception): pass

# signature errors
class SignatureVerificationFailedError (Exception): pass

# encryption errors
class SymmetricEncryptionError (Exception): pass
class AsymmetricEncryptionError (Exception): pass

####################################

# class PacketParseException (Exception): pass
