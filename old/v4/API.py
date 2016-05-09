#!/usr/local/bin/python

####################################
# standard
import settings

####################################
# custom
import DBM
import PWU
import utils


def open_db(config=None):
    dbm = DBM.DBManager(config=config)
    dbm.do_read()
    return dbm

def save_db(dbm, config=None):
    dbm.write(config=config)

def create_entry(dbm, config=None):
    # prep config
    config = utils.configify(config)

    # must be present:
    serv    = config['service']
    unam    = config['username']
    secret  = config['secret']
    salt    = PWU.gen_salt()
    iters   = PWU.DEFAULT_ITERATIONS
    length  = int(config.get('length', PWU.DEFAULT_PW_LENGTH))
    chars   = config.get('chars', '')
    old_pw  = config.get('old_pw', '')

    print chars
    if chars:
        chars = ''.join(sorted(set(PWU.ALPHANUM_AND_DIGITS + chars)))
    print chars

    assert serv
    assert unam
    assert secret
    assert salt
    assert length

    ####################################
    # hash password
    # (guarantee params are good)
    assert PWU.simple_hash(secret, salt, iters, length, chars=chars)

    ####################################
    # add entry
    params = {
        "service":      serv,
        "username":     unam,
        "salt":         salt,
        "iterations":   str(iters),
        "length":       str(length),
        "charset":      chars,
        "old_pw":       old_pw,
    }

    return dbm.add(params)

def hash_entry(dbm, config=None):
    # prep config
    config = utils.configify(config)

    serv   = config['service']
    unam   = config['username']
    secret = config['secret']

    # assert serv # might only have one entry!
    # assert unam # 'serv' could narrow down enough!
    assert secret

    ####################################
    # search for the entry
    params = {"service":serv, "username":unam}

    results = dbm.search(params)
    if not results:
        print "No results."
        return
    elif len(results) > 1:
        print "Too many results."
        return

    ####################################
    # prepare parameters
    match = results[0][1]

    salt   = match.salt # MUST be stored
    iters  = match.iterations
    length = match.length
    chars  = match.charset

    assert salt # this is non-negotiable.

    iters  = int(iters)  if iters  else PWU.DEFAULT_ITERATIONS
    length = int(length) if length else PWU.DEFAULT_PW_LENGTH
    chars  = chars       if chars  else PWU.ALPHANUM_AND_DIGITS

    return PWU.simple_hash(secret, salt, iters, length, chars=chars)

# def lookup_entry(dbm, config=None):
#     # prep config
#     config = utils.configify(config)



if __name__ == '__main__':

    dbm = open_db({"password":"password"})
    # save_db(dbm, {"path":"/Users/Matt/test.csv"})


    # print dbm.search({"username":"99"})[0][1].old_pw
    # print dbm.find('vim','dec')

    print hash_entry(dbm, {"service":"v", "username":"deck", "secret":"somelongpassLONG!"})

    # print create_entry(dbm, {"service":"vimeo", "username":"decka", "secret":"somelongpassLONG!", "chars":"abc123"})

    # dbm.write({"b16_elems":False})