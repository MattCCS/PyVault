
from pyvault.db.tables import table


class EmptyTable(table.Table):

    def __init__(self):
        pass

    def set_password(self):
        raise NotImplementedError()

    def save(self):
        return {}
