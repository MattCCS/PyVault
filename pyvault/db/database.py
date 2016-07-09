"""
"""

# custom
from pyvault import errors
from pyvault.db import entry
from pyvault.db import saveable
from pyvault.db import utils
from pyvault.db.key_manager import KEYMAN


class Table(saveable.Saveable):
    """
    """

    ON_DISK = 0
    LOCKED = 1
    OPEN = 2

    def __init__(self):
        self.state = Table.ON_DISK
        self.encrypted_table = None
        self.entries = None
        self.namepairs = None

    def _assert_on_disk(self):
        if self.state != Table.ON_DISK:
            raise errors.PasswordFileNotOnDisk()

    def _assert_locked(self):
        if self.state != Table.LOCKED:
            raise errors.PasswordFileNotLocked()

    def _assert_open(self):
        if self.state != Table.OPEN:
            raise errors.PasswordFileNotOpen()

    def _assert_not_service_account_pair(self, service, account):
        if self.service_account_pair_exists(service, account):
            raise errors.ServiceAccountPairAlreadyExists()

    ####################################
    # ON_DISK state methods

    def load(self, encrypted_table):
        """
        ON_DISK -> LOCKED
        """
        self._assert_on_disk()
        self.encrypted_table = encrypted_table
        self.state = Table.LOCKED

    ####################################
    # LOCKED state methods

    def save(self):
        """
        LOCKED -> ON_DISK
        """
        self._assert_locked()
        raise NotImplementedError()
        self.state = Table.ON_DISK
        # return {
        #     'entries': [entry.save() for entry in self.entries]
        # }

    def decrypt(self, memkey):
        """
        LOCKED -> OPEN
        """
        self._assert_locked()

        # decrypt table (errors are handled implicitly)
        decrypted_table = utils.decrypt_with_stretching(memkey, KEYMAN.get_key_data(), self.encrypted_table)

        # move to OPEN state
        self.encrypted_table = None
        self.entries = []
        self.namepairs = set()
        self.state = Table.OPEN

        # load entries
        for entry_data in decrypted_table['entries']:
            entry_ = entry.Entry(entry_data)
            self._add_entry(entry_)

    ####################################
    # OPEN state methods

    def encrypt(self, memkey):
        """
        OPEN -> LOCKED
        """
        self._assert_open()
        raise NotImplementedError()
        self.state = Table.LOCKED

    def service_account_pair_exists(self, service, account):
        self._assert_open()
        return (service.lower(), account.lower()) in self.namepairs

    def _add_entry(self, entry):
        """Adds a completed entry."""
        self._assert_open()
        self._assert_not_service_account_pair(entry.service, entry.account)

        # update entries and namepairs
        self.entries.append(entry)
        self.namepairs.add((entry.service.lower(), entry.account.lower()))

    def add_encrypted_entry(self, memkey, service, account, password, notes=''):
        self._assert_open()
        self._assert_not_service_account_pair(service, account)

        # create entry
        entry_ = entry.EncryptedEntry.new(memkey, service, account, password, notes=notes)
        self._add_entry(entry_)

TABLE = Table()
