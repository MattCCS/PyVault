
# standard
import os
import sys

# project
from pyvault import settings

# make cryptography library and others available
sys.path.append(os.path.join(settings.BASE_DIR, "site-packages"))


def patch_crypto_be_discovery():
    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    Source:  https://github.com/pyca/cryptography/issues/2039
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]

patch_crypto_be_discovery()
