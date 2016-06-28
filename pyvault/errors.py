"""
This file contains custom exception classes used for
differentiating expected and unexpected cryptographic exceptions.
"""

####################################

# file errors
# class PasswordDatabaseNotFound (Exception): pass
class PasswordFileNotJSON (Exception): pass
class PasswordFilePermission (Exception): pass

# state errors
class PasswordFileNotLoaded (Exception): pass
class PasswordFileAlreadyLoaded (Exception): pass
class PasswordTableNotDecrypted (Exception): pass
class PasswordTableAlreadyDecrypted (Exception): pass
