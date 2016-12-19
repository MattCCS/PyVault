"""
Contains settings for the password manager.
"""

import json
import os

BASE_FOLDER = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(BASE_FOLDER, "config.json")

with open(CONFIG_PATH) as config:
    SETTINGS = json.loads(config.read())

VAULT_FOLDER = SETTINGS['vault_folder']
VAULT_FILE = SETTINGS['vault_file']
VAULT_PATH = os.path.join(VAULT_FOLDER, VAULT_FILE)
