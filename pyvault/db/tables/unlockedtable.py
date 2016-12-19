
from pyvault.db.entries import entry
from pyvault.db.tables import table


class UnlockedTable(table.TableWithPassword):

    def __init__(self, keys, passdata, clearkeys):
        super(UnlockedTable).__init__(keys, passdata)
        self.clearkeys = map(entry.Entry.load, clearkeys)

    def encrypt(self):
        raise NotImplementedError()

    def reencrypt_keys(self, key, newkey):
        raise NotImplementedError()

    def add_entry(self):
        raise NotImplementedError()

    def list_entry(self):
        raise NotImplementedError()

    def list_entries(self):
        raise NotImplementedError()

    def edit_entry(self):
        raise NotImplementedError()

    def delete_entry(self):
        raise NotImplementedError()
