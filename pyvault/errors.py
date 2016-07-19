"""
This file contains custom exception classes used for
differentiating expected and unexpected cryptographic exceptions.
"""

####################################

# file errors
# class PasswordTableNotFound (Exception): pass
class PasswordFileNotJSON (Exception): pass
class PasswordFilePermission (Exception): pass

# state errors
class PasswordFileNotOnDisk (Exception): pass
class PasswordFileNotLocked (Exception): pass
class PasswordFileNotOpen (Exception): pass

class MasterPasswordIncorrect (Exception): pass

class ServiceAccountPairAlreadyExists (Exception): pass
