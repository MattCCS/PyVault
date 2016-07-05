"""
"""

# package
from pyvault import errors
from pyvault.crypto import key_stretching
from pyvault.crypto import packing_utils
from pyvault.db import utils


class KeyManager(object):

    ON_DISK = 0
    OPEN = 1

    def __init__(self):
        self.state = KeyManager.ON_DISK
        self.key_data = None

    ####################################
    # state methods
    def _assert_on_disk(self):
        if self.state != KeyManager.ON_DISK:
            raise errors.PasswordFileNotOnDisk()

    def _assert_open(self):
        if self.state != KeyManager.OPEN:
            raise errors.PasswordFileNotOpen()

    ####################################
    # data methods

    def get_key_data(self):
        return dict(self.key_data)

    ####################################
    # ON_DISK methods

    def load(self, key_data):
        """
        ON_DISK -> OPEN
        """
        self._assert_on_disk()
        self.key_data = key_data
        self.state = KeyManager.OPEN

    ####################################
    # OPEN methods

    def check_master_password(self, memkey):
        """
        Equivalent to self.derive_master_password, but does not return the key.
        """
        self._assert_open()
        self.derive_master_password(memkey)

    def derive_master_password(self, memkey):
        """
        Derives the master password, confirms its correctness, and returns it.
        """
        self._assert_open()

        master_key_hash = packing_utils.unpack(self.key_data['hash'])
        salt = packing_utils.unpack(self.key_data['salt'])
        mode = self.key_data['mode']
        iterations = self.key_data['iterations']
        length = self.key_data['length']

        # derive master password (with nonce)
        (master_key, _) = key_stretching.stretch(memkey, salt, mode=mode, iterations=iterations, length=length)

        # stretch again to confirm
        utils.compare_hash_and_key(master_key_hash, master_key, salt, mode, iterations, length)

        return master_key


KEYMAN = KeyManager()
