"""
"""

# standard
import abc
import base64

# package
from pyvault.crypto import datetime_utils
from pyvault.crypto import encryption_utils
from pyvault.crypto import key_stretching
# from pyvault.crypto import packing_utils
from pyvault.db import saveable
from pyvault.db.key_manager import KEYMAN
from pyvault.utils import passwords


def Entry(data):
    """
    Instantiates either an EncryptedEntry or DerivedEntry,
    whichever is appropriate given the Entry data.
    """
    if 'encrypted_password' in data:
        return EncryptedEntry(data)
    else:
        return DerivedEntry(data)


class _AbstractEntry(saveable.Saveable):
    """
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self.service = data['service']
        self.account = data['account']
        self.date_created = data['date_created']
        self.date_modified = data['date_modified']
        self.notes = data['notes']

    @staticmethod
    def new(service, account, notes=''):
        now = datetime_utils.now()
        data = {
            'service': service,
            'account': account,
            'date_created': now,
            'date_modified': now,
            'notes': notes,
        }
        return _AbstractEntry(data)

    def save(self):
        return {
            'service': self.service,
            'account': self.account,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'notes': self.notes,
        }

########################################


class EncryptedEntry(_AbstractEntry):

    def __init__(self, data):
        _AbstractEntry.__init__(self, data)
        self.encrypted_password = data['encrypted_password']

    @staticmethod
    def new(memkey, service, account, password, notes=''):
        master_key = KEYMAN.derive_master_password(memkey)

        encrypted_password = encryption_utils.encrypt(master_key, password)

        data = _AbstractEntry.new(service, account, notes=notes).save()
        data.update({
            'encrypted_password': encrypted_password,
        })
        return EncryptedEntry(data)

    def save(self):
        data = _AbstractEntry.save(self)
        data.update({
            'encrypted_password': self.encrypted_password,
        })
        return data

    ############################################
    # utilities

    def decrypt(self, memkey):
        master_key = KEYMAN.derive_master_password(memkey)
        password = encryption_utils.decrypt(master_key, self.encrypted_password)
        return password


class DerivedEntry(_AbstractEntry):

    def __init__(self, data):
        _AbstractEntry.__init__(self, data)
        passdata = data['derived_password_data']
        self.mode = passdata['mode']
        self.salt = base64.b64decode(passdata['salt'])
        self.iterations = passdata['iterations']
        self.length = passdata['length']

        passparams = data['derived_password_parameters']
        self.uppercase = passparams['uppercase']
        self.lowercase = passparams['lowercase']
        self.digits = passparams['digits']
        self.punctuation = passparams['punctuation']
        self.custom = passparams['custom']
        self.all = passparams['all']

    @staticmethod
    def new(self):
        raise NotImplementedError()

    def save(self):
        data = _AbstractEntry.save(self)
        data.update({
            'derived_password_parameters': {
                'uppercase': self.uppercase,
                'lowercase': self.lowercase,
                'digits': self.digits,
                'punctuation': self.punctuation,
                'custom': self.custom,
                'all': self.all,
            },
            'derived_password_data': {
                'mode': self.mode,
                'salt': base64.b64encode(self.salt),
                'iterations': self.iterations,
                'length': self.length,
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
        if self.all:
            chars = passwords.ALL
        else:
            chars = passwords.password_chars(
                upper=self.uppercase,
                lower=self.lowercase,
                digits=self.digits,
                punctuation=self.punctuation,
                custom=frozenset(self.custom),
            )

        return passwords.remap_bytearray(bytearray(key), chars)


if __name__ == '__main__':
    TEST_ENCRYPTED = {

    }

    TEST_DERIVED = {
        'service': 'Yahoo',
        'account': 'bob',
        'notes': 'for yahoo answers exclusively',
        'date_created': 1463005763,
        'date_modified': 1463005829,
        'derived_password_data': {
            'salt': '6FwbKr//dLNP+Iah3bO5XA==',
            'mode': 'sha256',
            'iterations': 100000,
            'length': 12,
        },
        'derived_password_parameters': {
            'uppercase': True,
            'lowercase': True,
            'digits': True,
            'punctuation': False,
            'custom': '',
            'all': False,
        }
    }

    d = Entry(TEST_DERIVED)
    print d
    print d.derive('secret')
    print d.save() == TEST_DERIVED
