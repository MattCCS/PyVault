
from pyvault.crypto import generic_utils
from pyvault.crypto import key_stretching
from pyvault.crypto import packing_utils
from pyvault.db import utils
from pyvault.db import properties


class Password(properties.Saveable, properties.Loadable, properties.Newable):

    @staticmethod
    def load(password_data):
        password_data['key_hash'] = packing_utils.unpack(password_data['key_hash'])
        password_data['salt'] = packing_utils.unpack(password_data['salt'])
        return Password(**password_data)

    @staticmethod
    def new(master_key):
        salt = generic_utils.nonce()
        (key_hash, (mode, _, iterations, length)) = key_stretching.stretch(master_key, salt)
        return Password(**{
            "key_hash": key_hash,
            "salt": salt,
            "mode": mode,
            "iterations": iterations,
            "length": length,
        })

    def __init__(self, key_hash, salt, mode, iterations, length):
        self.key_hash = key_hash
        self.salt = salt
        self.mode = mode
        self.iterations = iterations
        self.length = length

    def reset(self, key, newkey):
        old_master_key = self.derive(key)
        newpass = Password.new(newkey)
        return (old_master_key, newpass)

    def check(self, key):
        """Equivalent to self.derive, but does not return the key."""
        self.derive(key)

    def derive(self, key):
        """Derives the master password, confirms its correctness, and returns it."""
        (master_key, _) = key_stretching.stretch(
            key,
            self.salt,
            mode=self.mode,
            iterations=self.iterations,
            length=self.length,
        )

        # stretch again to confirm
        utils.compare_hash_and_key(
            self.key_hash,
            master_key,
            self.salt,
            self.mode,
            self.iterations,
            self.length,
        )

        return master_key
