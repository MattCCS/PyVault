
from pyvault.db import errors


TABLE = None


def set_table(table):
    global TABLE
    if TABLE:
        raise errors.TableAlreadyLoadedError()
    TABLE = table
    return TABLE


def get_table():
    global TABLE
    if not TABLE:
        raise errors.NoTableLoadedError()
    return TABLE
