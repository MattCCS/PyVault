
from pyvault.db.tables import table


class LockedTable(table.TableWithPassword):

    def __init__(self, keys, passdata):
        super(LockedTable).__init__(keys, passdata)

    def decrypt(self):
        raise NotImplementedError()

    def reencrypt_keys(self, key, newkey):
        raise NotImplementedError()
