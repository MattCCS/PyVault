
# standard
import json

# custom
from pyvault import errors
from pyvault.crypto import generic_utils
from pyvault.crypto import key_stretching
from pyvault.crypto import packing_utils
from pyvault.crypto import encryption_utils


def compare_hash_and_key(target, key, salt, mode, iterations, length):
    (target_2, _) = key_stretching.stretch(key, salt, mode=mode, iterations=iterations, length=length)
    if target != target_2:
        raise errors.MasterPasswordIncorrect("Master password was incorrect!")


def encrypt_with_stretching(memkey, table):
    # derive master password (with nonce)
    (master_key, key_data) = key_stretching.stretch(memkey, generic_utils.nonce())
    (mode, salt, iterations, length) = key_data

    # stretch master password
    (master_key_hash, _) = key_stretching.stretch(master_key, salt)

    # dump data, encrypt and HMAC
    table_encrypted = encryption_utils.encrypt(master_key, table)
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
    compare_hash_and_key(master_key_hash, master_key_2, salt, mode, iterations, length)

    # decrypt the table
    print "Decrypting..."
    ciphertext_data = packing_utils.unpack(p_table_encrypted)
    table = encryption_utils.decrypt(master_key_2, ciphertext_data)
    return table


if __name__ == '__main__':
    table_1 = {
        'entries': [
            {
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
        ],
    }
    print table_1

    save = encrypt_with_stretching("password", table_1)
    print json.dumps(save, indent=4)

    table_2 = decrypt_with_stretching("password", save['key data'], save['table'])
    print table_2

    print table_2 == table_1
