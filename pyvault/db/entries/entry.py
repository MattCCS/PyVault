
import abc

from pyvault.crypto import datetime_utils
from pyvault.db import properties
from pyvault.db.entries import derivedentry
from pyvault.db.entries import encryptedentry
#from pyvault.db import state


class Entry(abc.ABC, properties.Saveable, properties.Loadable):

    def load(entry_data):
        if 'password' in entry_data:
            return encryptedentry.EncryptedEntry(**entry_data)
        else:
            return derivedentry.DerivedEntry(**entry_data)

    @staticmethod
    def new(service, account, notes=''):
        now = datetime_utils.now()
        return {
            'service': service,
            'account': account,
            'notes': notes,
            'date_created': now,
            'date_modified': now,
        }

    def __init__(self, service, account, notes, date_created, date_modified):
        self.service = service
        self.account = account
        self.notes = notes
        self.date_created = date_created
        self.date_modified = date_modified

    def save(self):
        return {
            'service': self.service,
            'account': self.account,
            'notes': self.notes,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
        }
