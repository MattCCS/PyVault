
from pyvault.crypto import encryption_utils
from pyvault.db.tables import table
from pyvault.db.tables import unlockedtable


class LockedTable(table.TableWithPassword):

    @staticmethod
    def load(table_data):
        return LockedTable(**table_data)

    @staticmethod
    def new(keys, passdata):
        return LockedTable(keys, passdata)

    def __init__(self, keys, passdata):
        super(LockedTable).__init__(keys, passdata)

    def decrypt(self, key):
        master_key = self.password.derive(key)
        clearkeys = encryption_utils.decrypt(master_key, self.keys)
        return unlockedtable.UnlockedTable.new(self.keys, self.passdata, clearkeys)

    def reencrypt_keys(self, key, newkey):
        master_key = self.password.derive(key)
        clearkeys = encryption_utils.decrypt(master_key, self.keys)
        self.keys = encryption_utils.encrypt(newkey, clearkeys)
