
import base64

from pyvault.crypto import crypto_settings
from pyvault.crypto import generic_utils
from pyvault.crypto import key_stretching
from pyvault.db.entries import entry
from pyvault.utils import passwords


class DerivedEntry(entry.Entry):

    @staticmethod
    def new(service, account, password, notes='', length=crypto_settings.DERIVED_BYTES, characters=passwords.ALL):
        data = super(DerivedEntry).new(service, account, password, notes=notes)
        data.update({
            'params': {
                'mode': crypto_settings.DEFAULT_HASH_MODE,
                'salt': generic_utils.nonce(),
                'iterations': crypto_settings.DEFAULT_ITERATIONS,
                'length': length,
                'characters': characters,
            }
        })
        return DerivedEntry(**data)

    def __init__(self, service, account, notes, date_created, date_modified, params):
        super(DerivedEntry).__init__(self, service, account, notes, date_created, date_modified)
        self.mode = params['mode']
        self.salt = params['salt']
        self.iterations = params['iterations']
        self.length = params['length']
        self.characters = params['characters']

    def save(self):
        data = super(DerivedEntry).save(self)
        data.update({
            'params': {
                'mode': self.mode,
                'salt': base64.b64encode(self.salt),
                'iterations': self.iterations,
                'length': self.length,
                'characters': self.characters,
            },
        })
        return data

    def _derive(self, memkey):
        return key_stretching.stretch(
            memkey,
            self.salt,
            mode=self.mode,
            iterations=self.iterations,
            length=self.length,
        )

    def derive(self, memkey):
        (key, _) = self._derive(memkey)
        return passwords.remap_bytearray(bytearray(key), self.characters)


if __name__ == '__main__':
    TEST_ENCRYPTED = {

    }

    TEST_DERIVED = {
        'service': 'Yahoo',
        'account': 'bob',
        'notes': 'for yahoo answers exclusively',
        'date_created': 1463005763,
        'date_modified': 1463005829,
        'params': {
            'salt': '6FwbKr//dLNP+Iah3bO5XA==',
            'mode': 'sha256',
            'iterations': 100000,
            'length': 12,
            'characters': 'abcdefghijklmnopqrstuvwxyz0123456789'
        },
    }

    d = DerivedEntry(**TEST_DERIVED)
    print d
    print d.derive('secret')
    print d.save() == TEST_DERIVED
