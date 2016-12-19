
import abc

from pyvault.db import errors
from pyvault.db import properties
from pyvault.db.tables import emptytable
from pyvault.db.tables import lockedtable


class Table(properties.Saveable, properties.Loadable):

    __metaclass__ = abc.ABCMeta

    def load(table_data):
        if not table_data:
            return emptytable.EmptyTable()
        return lockedtable.LockedTable.load(**table_data)

    def set_password(self, key):
        raise errors.RequiresEmptyTableError()

    def reset_password(self, key, newkey):
        raise errors.RequiresTableWithPasswordError()

    def check_password(self, key):
        raise errors.RequiresTableWithPasswordError()

    def decrypt(self, key):
        raise errors.RequiresLockedTableError()

    def encrypt(self, key):
        raise errors.RequiresUnlockedTableError()

    def add_entry(self, key, entry):
        raise errors.RequiresUnlockedTableError()

    def list_entry(self, id_):
        raise errors.RequiresUnlockedTableError()

    def list_entries(self, query):
        raise errors.RequiresUnlockedTableError()

    def edit_entry(self, key, id_, newentry):
        raise errors.RequiresUnlockedTableError()

    def delete_entry(self, key, id_):
        raise errors.RequiresUnlockedTableError()
