
import abc

from pyvault.db import password
from pyvault.db.tables import table


class TableWithPassword(table.Table):

    __metaclass__ = abc.ABCMeta

    def __init__(self, keys, passdata):
        self.keys = keys
        self.passdata = password.Password.load(passdata)

    def reset_password(self, key, newkey):
        self.passdata = self.passdata.reset(key, newkey)
        self.reencrypt_keys(key, newkey)
        self.save()

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
