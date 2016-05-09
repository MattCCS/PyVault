
import binascii
import collections

####################################

def hexed(s):
    return binascii.hexlify(s)

def unhexed(hexstring):
    return binascii.unhexlify(hexstring)


gen_config = lambda : collections.defaultdict(lambda : None)


def configify(params):
    dd = gen_config()

    if params is not None:
        dd.update(**params)
        
    return dd
