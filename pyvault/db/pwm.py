"""
"""

# standard
import json

# package
from pyvault import errors
from pyvault import settings
# from pyvault.db import utils
from pyvault.db.table import TABLE
from pyvault.db.key_manager import KEYMAN
from pyvault.crypto import encryption_utils


class PasswordManager(object):
    """Singleton class that acts as the PyVault API."""

    ####################################
    # file methods
    def load(self):
        """Load password table from disk."""
        try:
            with open(settings.DB_PATH) as db_file:
                db_json = db_file.read()
        except IOError:
            # TODO: handle other file errors
            raise errors.PasswordFilePermission()

        try:
            db = json.loads(db_json)
        except ValueError:
            raise errors.PasswordFileNotJSON()

        # load to modules
        KEYMAN.load(db['key data'])
        TABLE.load(db['table'])

    def save(self):
        """Save password table to disk."""
        raise NotImplementedError() # TODO: <<<!!!
        db = {
            'key data': KEYMAN.save(),
            'table': TABLE.save(),
        }

        db_json = json.dumps(db)

        try:
            with open(settings.DB_PATH, 'w') as db_file:
                db_file.write(db_json)
        except IOError:
            # TODO: handle other file errors
            raise errors.PasswordFilePermission()

    ####################################
    # ...

    def encrypt_data(self, memkey, *data):
        self.check_file_loaded()
        master_key = self.derive_master_password(memkey)
        return (encryption_utils.encrypt(master_key, datum) for datum in data)

    # entry methods
    def check_service_account_pair(self, service, account):
        self.check_table_decrypted()
        return self.table.check_service_account_pair(service, account)

    # def add_encrypted_entry(self, memkey, service, account, password, notes=''):
    #     # self.check_table_decrypted()

    #     # # encrypt password
    #     # (e_password, e_notes) = self.encrypt(memkey, password, notes)

    #     # # create entry
    #     # self.table.add_entry(service, account, e_password, e_notes)

    #     raise NotImplementedError()

    def add_derived_entry(self, service, account, notes=''):
        raise NotImplementedError()

    def show_entry(self): raise NotImplementedError()

    def edit_entry(self): raise NotImplementedError()

    def delete_entry(self): raise NotImplementedError()


PWM = PasswordManager()
