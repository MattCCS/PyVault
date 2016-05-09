"""
This file contains custom exceptions and transition exceptions.
"""

########################################
# transisitions

# login page
class LoginToMain(Exception): pass

# main page
class MainToLogin(Exception): pass
