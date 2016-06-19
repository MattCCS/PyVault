"""
This file contains custom exception classes used for
differentiating expected and unexpected cryptographic exceptions.
"""

####################################

# file errors
# class PasswordDatabaseNotFound (Exception): pass
class PasswordDatabaseNotJSON (Exception): pass
class PasswordDatabasePermission (Exception): pass

# state errors
class PasswordDatabaseNotLoaded (Exception): pass
class PasswordTableAlreadyDecrypted (Exception): pass
