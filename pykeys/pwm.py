"""
"""

# standard
import json
import functools

# package
from pykeys import errors
from pykeys import settings
from pykeys.db import utils
from pykeys.crypto import packing_utils
from pykeys.crypto import key_stretching


# decorators
def decorator_factory(requirement_func, error_arg):
    def generic_decorator(func):
        @functools.wraps(func)
        def _decorator(self, *args, **kwargs):
            if not requirement_func(self):
                raise error_arg()
            return func(self, *args, **kwargs)
        return _decorator
    return generic_decorator

requires_file_not_loaded = decorator_factory(lambda self: not self.table, errors.PasswordFileAlreadyLoaded)
requires_file_loaded = decorator_factory(lambda self: self.table, errors.PasswordFileNotLoaded)
requires_table_encrypted = decorator_factory(lambda self: not isinstance(self.table, dict), errors.PasswordTableAlreadyDecrypted)
requires_table_decrypted = decorator_factory(lambda self: isinstance(self.table, dict), errors.PasswordTableNotDecrypted)


class PasswordManager(object):
    """Singleton class that acts as the PyKeys API."""

    def __init__(self):
        self.key_data = None
        self.table = None

    # file methods
    @requires_file_not_loaded
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
            self.key_data = db['key data']
            self.table = db['table']
        except ValueError:
            raise errors.PasswordFileNotJSON()

    @requires_file_loaded
    def save(self):
        """Save password table to disk."""
        raise NotImplementedError()

    # database methods
    @requires_file_loaded
    @requires_table_encrypted
    def decrypt(self, memkey):
        # decrypt table (errors are handled implicitly)
        self.table = utils.decrypt_with_stretching(memkey, self.key_data, self.table)
        return self.table

    @requires_file_loaded
    @requires_table_decrypted
    def encrypt(self): raise NotImplementedError()

    # utility methods
    @requires_file_loaded
    def check_master_password(self, memkey):
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
    def show_entry(self): raise NotImplementedError()
    def add_entry(self): raise NotImplementedError()
    def edit_entry(self): raise NotImplementedError()
    def delete_entry(self): raise NotImplementedError()


PWM = PasswordManager()
