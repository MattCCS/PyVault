
from pyvault.db.entries import entry


class EncryptedEntry(entry.Entry):

    @staticmethod
    def new(service, account, password, notes=''):
        data = super(EncryptedEntry).new(service, account, notes=notes).save()
        data.update({
            'password': password,
        })
        return EncryptedEntry(**data)

    def __init__(self, service, account, notes, date_created, date_modified, password):
        super(EncryptedEntry).__init__(service, account, notes, date_created, date_modified)
        self.password = password

    def save(self):
        data = super(EncryptedEntry).save(self)
        data.update({
            'password': self.password,
        })
        return data
