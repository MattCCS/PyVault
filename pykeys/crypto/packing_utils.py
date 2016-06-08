
# standard
import base64

# custom
from pykeys.crypto import constants

####################################

def pack(*parts):
    return constants.DELIMITER.join(base64.b64encode(e) for e in parts)

def unpack(data):
    out = tuple(base64.b64decode(e) for e in data.split(constants.DELIMITER))
    if len(out) == 1:
        return out[0]
    else:
        return out
