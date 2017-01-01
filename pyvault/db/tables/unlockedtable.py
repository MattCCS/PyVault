
import warnings

from pyvault.crypto import encryption_utils
from pyvault.db.entries import entry
from pyvault.db.tables import table
from pyvault.db.tables import lockedtable


class UnlockedTable(table.TableWithPassword):

    @staticmethod
    def new(keys, passdata, clearkeys):
        return UnlockedTable(keys, passdata, clearkeys)

    def __init__(self, keys, passdata, clearkeys):
        super(UnlockedTable).__init__(keys, passdata)
        self.clearkeys = map(entry.Entry.load, clearkeys)

    def encrypt(self, key):
        master_key = self.password.derive(key)
        keys = encryption_utils.encrypt(master_key, self.clearkeys)
        return lockedtable.LockedTable.new(keys, self.passdata)

    def reencrypt_keys(self, old_master_key, newkey):
        new_master_key = self.passdata.derive(newkey)
        self.keys = encryption_utils.encrypt(new_master_key, self.clearkeys)

    def update_keys(self, key, newkeys):
        master_key = self.passdata.derive(key)
        self.keys = encryption_utils.encrypt(master_key, newkeys)
        self.clearkeys = newkeys

    def add_entry(self, key, entry):
        tempkeys = self.clearkeys[:]
        tempkeys.append(entry)
        self.update_keys(key, tempkeys)

    def show_entry(self, key, index):
        self.check_password(key)
        return self.clearkeys[index]

    def list_entries(self, query):
        # TODO
        warnings.warn("'query' param will be ignored!")
        return [clearkey.save() for clearkey in self.clearkeys]

    def edit_entry(self, key, index, newentry):
        tempkeys = self.clearkeys[:]
        tempkeys[index] = newentry
        self.update_keys(key, tempkeys)

    def delete_entry(self, key, index):
        tempkeys = self.clearkeys[:]
        del tempkeys[index]
        self.update_keys(key, tempkeys)
