"""
PyVault API functions.
"""

# package
from pyvault.db import KEYMAN
from pyvault.db import PWM
from pyvault.db import TABLE


# define functions locally "for __all__ to see" ;)
load = PWM.load
save = PWM.save

decrypt = TABLE.decrypt
encrypt = TABLE.encrypt

add_encrypted_entry = TABLE.add_encrypted_entry

check_master_password = KEYMAN.check_master_password
derive_master_password = KEYMAN.derive_master_password

service_account_pair_exists = TABLE.service_account_pair_exists


__all__ = [
    "load",
    "save",

    "decrypt",
    "encrypt",

    "add_encrypted_entry",
    # "add_derived_entry",

    "check_master_password",
    "derive_master_password",

    "service_account_pair_exists",

]
