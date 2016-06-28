"""
"""

# standard
import json

# package
from pyvault import errors
from pyvault import settings
from pyvault.db import utils
from pyvault.crypto import packing_utils
from pyvault.crypto import key_stretching


class PasswordManager(object):
    """Singleton class that acts as the PyVault API."""

    def __init__(self):
        self.key_data = None
        self.table = None

    def check_file_not_loaded(self):
        if self.table:
            raise errors.PasswordFileAlreadyLoaded()

    def check_file_loaded(self):
        if not self.table:
            raise errors.PasswordFileNotLoaded()

    def check_table_encrypted(self):
        if isinstance(self.table, dict):
            raise errors.PasswordTableAlreadyDecrypted()

    def check_table_decrypted(self):
        if not isinstance(self.table, dict):
            raise errors.PasswordTableNotDecrypted()

    ####################################################

    # file methods
    def load(self):
        """Load password table from disk."""
        self.check_file_not_loaded()

        try:
            with open(settings.DB_PATH) as db_file:
                db_json = db_file.read()
        except IOError:
            # TODO: handle other file errors
            raise errors.PasswordFilePermission()

        try:
            db = json.loads(db_json)
            self.key_data = db['key data']
            self.table = db['table']
        except ValueError:
            raise errors.PasswordFileNotJSON()

    def save(self):
        """Save password table to disk."""
        self.check_file_loaded()

        raise NotImplementedError()

    # database methods
    def decrypt(self, memkey):
        self.check_file_loaded()
        self.check_table_encrypted()

        # decrypt table (errors are handled implicitly)
        self.table = utils.decrypt_with_stretching(memkey, self.key_data, self.table)
        return self.table

    def encrypt(self):
        self.check_file_loaded()
        self.check_table_encrypted()

        raise NotImplementedError()

    # utility methods
    def check_master_password(self, memkey):
        self.check_file_loaded()

        master_key_hash = packing_utils.unpack(self.key_data['hash'])
        salt = packing_utils.unpack(self.key_data['salt'])
        mode = self.key_data['mode']
        iterations = self.key_data['iterations']
        length = self.key_data['length']

        # derive master password (with nonce)
        (master_key, _) = key_stretching.stretch(memkey, salt, mode=mode, iterations=iterations, length=length)

        # stretch again to confirm
        (master_key_hash_2, _) = key_stretching.stretch(master_key, salt, mode=mode, iterations=iterations, length=length)
        return master_key_hash == master_key_hash_2

    # entry methods
    def check_service_account_pair(self, service, account):
        raise NotImplementedError()

    def add_encrypted_entry(self, memkey, service, account, password, notes=''):
        pass

    def add_derived_entry(self, service, account, notes=''):
        raise NotImplementedError()

    def show_entry(self): raise NotImplementedError()

    def edit_entry(self): raise NotImplementedError()

    def delete_entry(self): raise NotImplementedError()


PWM = PasswordManager()
