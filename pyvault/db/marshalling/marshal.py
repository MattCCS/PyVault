
import os
import json

from pyvault import settings
from pyvault.db import errors


ERRNO_NO_SUCH_FILE = 2
ERRNO_NO_PERMISSION = 13
ERRNO_ALREADY_EXISTS = 17


def create():
    try:
        os.mkdirs(settings.VAULT_FOLDER)
    except OSError as exc:
        if exc.errno == ERRNO_NO_PERMISSION:
            raise errors.BadVaultFilePermissionsError()
        elif exc.errno == ERRNO_ALREADY_EXISTS:
            raise errors.VaultFileAlreadyExistsError()
        else:
            raise errors.DiskError(exc)

    return save({})


def load():
    try:
        with open(settings.VAULT_PATH) as vault_file:
            return json.loads(vault_file.read())
    except IOError as exc:
        if exc.errno == ERRNO_NO_SUCH_FILE:
            raise errors.NoVaultFileError()
        elif exc.errno == ERRNO_NO_PERMISSION:
            raise errors.BadVaultFilePermissionsError()
        else:
            raise errors.DiskError(exc)


def save(table_data):
    try:
        with open(settings.VAULT_PATH, 'w') as vault_file:
            vault_file.write(json.dumps(table_data, indent=4))
            return table_data
    except IOError as exc:
        if exc.errno == ERRNO_NO_PERMISSION:
            raise errors.BadVaultFilePermissionsError()
        else:
            raise errors.DiskError(exc)
