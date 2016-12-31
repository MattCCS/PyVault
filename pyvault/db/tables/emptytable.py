
from pyvault.db.tables import table
from pyvault.db.tables import tablewithpassword


class EmptyTable(table.Table):

    @staticmethod
    def load():
        return EmptyTable()

    @staticmethod
    def new():
        return EmptyTable()

    def __init__(self):
        pass

    def set_password(self, password):
        return tablewithpassword.TableWithPassword.new(password)

    def save(self):
        return {}
