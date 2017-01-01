
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

    def reencrypt_keys(self, key, newkey):
        master_key = self.password.derive(key)
        self.keys = encryption_utils.encrypt(master_key, self.clearkeys)

    def add_entry(self, key, entry):
        raise NotImplementedError()

    def show_entry(self, key, id_):
        raise NotImplementedError()

    def list_entries(self, query):
        raise NotImplementedError()

    def edit_entry(self, key, id_, newentry):
        raise NotImplementedError()

    def delete_entry(self, key, id_):
        raise NotImplementedError()
