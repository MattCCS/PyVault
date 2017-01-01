
import abc

from pyvault.db import password
from pyvault.db.tables import table
from pyvault.db.tables import lockedtable


class TableWithPassword(abc.ABC, table.Table):

    @staticmethod
    def load(table_data):
        return lockedtable.LockedTable.load(table_data)

    @staticmethod
    def new(password):
        data = {
            'keys': [],
            'passdata': password.Password.new(password),
        }
        return TableWithPassword(**data)

    def __init__(self, keys, passdata):
        self.keys = keys
        self.passdata = password.Password.load(passdata)

    def reset_password(self, key, newkey):
        (old_master_key, self.passdata) = self.passdata.reset(key, newkey)
        self.reencrypt_keys(old_master_key, newkey)

    def check_password(self, key):
        self.passdata.check(key)

    @abc.abstractmethod
    def reencrypt_keys(self, key, newkey):
        pass

    def save(self):
        return {
            'keys': self.keys,
            'passdata': self.passdata.save(),
        }
