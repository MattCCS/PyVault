
from pyvault.db.marshalling import marshal
from pyvault.db import state
from pyvault.db.tables import table


def create_table():
    table_data = marshal.create()
    table_obj = table.Table.load(table_data)
    return state.set_table(table_obj)


def load_table():
    table_data = marshal.load()
    table_obj = table.Table.load(table_data)
    return state.set_table(table_obj)


def save_table():
    table_data = state.get_table().save()
    return marshal.save(table_data)


def set_password(key):
    table = state.get_table().set_password(key)
    state.set_table(table)
    return table


def reset_password(key, newkey):
    return state.get_table().reset_password(key, newkey)


def check_password(key):
    return state.get_table().check_password(key)


def decrypt(key):
    return state.get_table().decrypt(key)


def encrypt(key):
    return state.get_table().encrypt(key)


def add_entry(self, key, entry):
    return state.get_table().add_entry(key, entry)


def show_entry(self, key, index):
    return state.get_table().show_entry(key, index)


def list_entries(self, query):
    return state.get_table().list_entries(query)


def edit_entry(self, key, index, newentry):
    return state.get_table().edit_entry(key, index, newentry)


def delete_entry(self, key, index):
    return state.get_table().delete_entry(key, index)
