
# standard
import json

# custom
from pykeys.crypto import errors
from pykeys.crypto import generic_utils
from pykeys.crypto import key_stretching
from pykeys.crypto import packing_utils
from pykeys.crypto import symmetric_encryption_utils


# def confirm_master_password(memkey, salt, master_key_hash):
#     return key_stretching.stretch(memkey, salt, )



def encrypt_with_stretching(memkey, data):
    # derive master password (with nonce)
    (master_key, ksd) = key_stretching.stretch(memkey, generic_utils.nonce())
    (mode, salt, iterations, length) = ksd

    # stretch master password
    (master_key_hash, _) = key_stretching.stretch(master_key, salt)

    # dump data, encrypt and HMAC
    ciphertext = symmetric_encryption_utils.encrypt_hmac(master_key, json.dumps(data))
    p_ciphertext = packing_utils.pack(ciphertext)

    keyfile = {
        'ksd': {
            'hash': packing_utils.pack(master_key_hash),
            'salt': packing_utils.pack(salt),
            'mode': mode,
            'iterations': iterations,
            'length': length,
        },
        'db': p_ciphertext,
    }

    # return packing_utils.pack(json.dumps(keyfile))
    return json.dumps(keyfile)


def decrypt_with_stretching(memkey, p_keyfile):
    # unpack the data
    # keyfile = json.loads(packing_utils.unpack(p_keyfile))
    keyfile = json.loads(p_keyfile)
    ksd = keyfile['ksd']
    master_key_hash = packing_utils.unpack(ksd['hash'])
    salt = packing_utils.unpack(ksd['salt'])
    mode = ksd['mode']
    iterations = ksd['iterations']
    length = ksd['length']

    # derive master password (with nonce)
    (master_key_2, _) = key_stretching.stretch(memkey, salt, mode=mode, iterations=iterations, length=length)

    # stretch again to confirm
    (master_key_hash_2, _) = key_stretching.stretch(master_key_2, salt, mode=mode, iterations=iterations, length=length)
    if master_key_hash != master_key_hash_2:
        raise errors.PasswordHashComparisonError("Master password was incorrect!")

    # decrypt the database
    ciphertext_data = packing_utils.unpack(keyfile['db'])
    db = json.loads(symmetric_encryption_utils.decrypt_hmac(master_key_2, ciphertext_data))

    keyfile['db'] = db  # overwrite encrypted volume in memory -- not on disk

    return keyfile

data = {'abc': 123}
print data

save = encrypt_with_stretching("password", data)
print save

load = decrypt_with_stretching("password", save)
print load

print load['db'] == data
