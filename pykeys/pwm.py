"""
"""

# standard
import json

# package
from pykeys import errors
from pykeys import settings
from pykeys.db import utils


class PasswordManager(object):
    """Singleton class that acts as the PyKeys API."""

    def __init__(self):
        self.key_data = None
        self.table = None

    # file methods
    def load(self):
        """Load password table from disk."""
        try:
            with open(settings.DB_PATH) as db_file:
                db_json = db_file.read()
        except IOError:
            # TODO: handle other file errors
            raise errors.PasswordDatabasePermission()

        try:
            db = json.loads(db_json)
            self.key_data = db['key data']
            self.table = db['table']
        except ValueError:
            raise errors.PasswordDatabaseNotJSON()

    def save():
        """Save password table to disk."""
        raise NotImplementedError()


    # database methods
    def decrypt(self, memkey):
        if not self.table:
            raise errors.PasswordDatabaseNotLoaded()
        if isinstance(self.table, dict):
            raise errors.PasswordTableAlreadyDecrypted()

        # decrypt table (errors are handled)
        self.table = utils.decrypt_with_stretching(memkey, self.key_data, self.table)
        return self.table

    def encrypt(self): raise NotImplementedError()

    # utility methods
    def check_master_password(self): raise NotImplementedError()

    # entry methods
    def show_entry(self): raise NotImplementedError()
    def add_entry(self): raise NotImplementedError()
    def edit_entry(self): raise NotImplementedError()
    def delete_entry(self): raise NotImplementedError()


PWM = PasswordManager()
