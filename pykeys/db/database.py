
# standard
import abc
import base64

# custom
from pykeys.utils import passwords
from pykeys.crypto import key_stretching
from pykeys.crypto import symmetric_encryption_utils


class Saveable(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def save(self):
        pass

########################################


class Database(Saveable):

    def __init__(self, data):
        self.entries = [Entry.new(d) for d in data['entries']]

    def save(self):
        return {
            'entries': [entry.save() for entry in self.entries]
        }

########################################


class Entry(Saveable):

    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self.service = data['service']
        self.account = data['account']
        self.notes = data['notes']
        self.date_created = data['date_created']
        self.date_modified = data['date_modified']

    @staticmethod
    def new(data):
        if 'p_encrypted_password' in data:
            return EncryptedEntry(data)
        elif 'derived_password_parameters' in data:
            return DerivedEntry(data)
        else:
            raise RuntimeError()

    def save(self):
        return {
            'service': self.service,
            'account': self.account,
            'notes': self.notes,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
        }


class EncryptedEntry(Entry):

    def __init__(self, data):
        Entry.__init__(self, data)
        self.p_encrypted_password = base64.b64decode(data['p_encrypted_password'])

    def save(self):
        out = {
            'p_encrypted_password': base64.b64encode(self.p_encrypted_password),
        }
        out.update(Entry.save(self))
        return out

    def decrypt(self, memkey):

        # return symmetric_encryption_utils.decrypt_hmac(, self.p_encrypted_password)
        pass


class DerivedEntry(Entry):

    def __init__(self, data):
        Entry.__init__(self, data)
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

    def save(self):
        out = {
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
        }
        out.update(Entry.save(self))
        return out

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

d = Entry.new(TEST_DERIVED)
print d
print d.derive('secret')
print d.save() == TEST_DERIVED
