
# standard
import json

# custom
from pyvault import errors
from pyvault.crypto import generic_utils
from pyvault.crypto import key_stretching
from pyvault.crypto import packing_utils
from pyvault.crypto import symmetric_encryption_utils


def encrypt_with_stretching(memkey, table):
    # derive master password (with nonce)
    (master_key, key_data) = key_stretching.stretch(memkey, generic_utils.nonce())
    (mode, salt, iterations, length) = key_data

    # stretch master password
    (master_key_hash, _) = key_stretching.stretch(master_key, salt)

    # dump data, encrypt and HMAC
    table_encrypted = symmetric_encryption_utils.encrypt_hmac(master_key, json.dumps(table))
    p_table_encrypted = packing_utils.pack(table_encrypted)

    db_encrypted = {
        'key data': {
            'hash': packing_utils.pack(master_key_hash),
            'salt': packing_utils.pack(salt),
            'mode': mode,
            'iterations': iterations,
            'length': length,
        },
        'table': p_table_encrypted,
    }

    return db_encrypted


def decrypt_with_stretching(memkey, key_data, p_table_encrypted):
    # unpack the data
    master_key_hash = packing_utils.unpack(key_data['hash'])
    salt = packing_utils.unpack(key_data['salt'])
    mode = key_data['mode']
    iterations = key_data['iterations']
    length = key_data['length']

    # derive master password (with nonce)
    print "Stretching password..."
    (master_key_2, _) = key_stretching.stretch(memkey, salt, mode=mode, iterations=iterations, length=length)

    # stretch again to confirm
    print "Confirming password..."
    (master_key_hash_2, _) = key_stretching.stretch(master_key_2, salt, mode=mode, iterations=iterations, length=length)
    if master_key_hash != master_key_hash_2:
        raise errors.PasswordHashComparisonError("Master password was incorrect!")

    # decrypt the database
    print "Decrypting..."
    ciphertext_data = packing_utils.unpack(p_table_encrypted)
    table = json.loads(symmetric_encryption_utils.decrypt_hmac(master_key_2, ciphertext_data))
    return table


if __name__ == '__main__':
    table_1 = {
        'abc': 123,
        'name': 'Matt',
        'favorite number': 7,
        'colors': ['red', 'green', 'blue'],
        'big_data': '''When in the Course of human events, it becomes necessary \
    for one people to dissolve the political bands which have connected them with \
    another, and to assume among the powers of the earth, the separate and equal \
    station to which the Laws of Nature and of Nature's God entitle them, a \
    decent respect to the opinions of mankind requires that they should declare \
    the causes which impel them to the separation.''',
    }
    print table_1

    save = encrypt_with_stretching("password", table_1)
    print json.dumps(save, indent=4)

    table_2 = decrypt_with_stretching("password", save['key data'], save['table'])
    print table_2

    print table_2 == table_1
