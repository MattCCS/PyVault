"""
Contains settings for the password manager.
"""

# standard
import os

SAFE_PATH = "~/.safe/"
DB_PATH = "keys.aes"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
