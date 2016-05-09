#!/usr/local/bin/python

####################################
# standard
import getpass

####################################
# custom
import API
# import BorderPatrol

def do_hash(dbm):
    params = {}

    ####################################
    # get service
    serv = raw_input("Service: ")

    params['service'] = serv
    results = dbm.search(params)
    if not results:
        print "No results."
        return
    for r in results:
        e = r[1]
        print "{} : {} : '{}'".format(e.service, e.username, e.old_pw)

    if len(results) > 1:
        unam = raw_input("Username: ")

        params['username'] = unam
        results = dbm.search(params)
        if not results:
            print "No results."
            return
        for r in results:
            e = r[1]
            print "{} : {} : '{}'".format(e.service, e.username, e.old_pw)

    if len(results) > 1:
        print "Too many results."
        return

    if not e.salt:
        print "No salt -- not set up!"
        return

    secret = getpass.getpass("(Secret): ")
    params['secret'] = secret

    _hash = API.hash_entry(dbm, params)

    print _hash # BAD !!!!!!!!!!!!!!!!!!!!!

def interactive(dbm):

    try:
        while True:

            print "c --> create"
            print "h --> hash"
            print "l --> list"
            print "s --> search"

            inp = raw_input("> ")

            if inp == 'c':
                do_create(dbm)

            elif inp == 'h':
                do_hash(dbm)

            elif inp == 'l':
                do_list(dbm)

            elif inp == 's':
                do_search(dbm)

            else:
                print "Nope."

    except KeyboardInterrupt:
        print "\nQuitting..."

def begin():

    table_pw = getpass.getpass("Table password (AES): ")

    dbm = API.open_db({"password": table_pw})

    interactive(dbm)

if __name__ == '__main__':
    begin()
