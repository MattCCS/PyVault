#!/usr/local/python

# standard
import functools
import getpass

# package
import pyvault
# print dir(pyvault)
from pyvault import errors

#######################################
# prompts and helpers
UNLOCK_MENU_PROMPT = """
Unlock Password Table
Password: """

MAIN_MENU_PROMPT = """
Main Menu
1) Add encrypted entry
2) Add derived entry
3) Check for service/account pair"""

CLEAR = "\n" * 24


def prompt_for(prompt, values, error="[-] Not a valid option.\n"):
    while True:
        inp = raw_input(prompt + "\n>")
        print CLEAR
        if inp in values:
            return inp
        else:
            print error


def control_c_backup(func):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print CLEAR
            return
    return wrap

#######################################
# screens


@control_c_backup
def check_service_account_menu():
    while True:
        print "\nCheck for Service/Account Pair"
        service = raw_input("Service: ")
        account = raw_input("Account: ")
        print pyvault.service_account_pair_exists(service, account)


@control_c_backup
def main_menu():
    choices = {
        # '1': 
        # '2': 
        '3': check_service_account_menu
    }

    while True:
        inp = prompt_for(MAIN_MENU_PROMPT, set('3'))
        choices[inp]()

    raise NotImplementedError()


@control_c_backup
def unlock_menu():
    # load file
    print "Loading..."
    pyvault.load()

    # unlock table
    print CLEAR
    while True:
        # prompt for memkey
        memkey = getpass.getpass(UNLOCK_MENU_PROMPT)
        try:
            pyvault.decrypt(memkey)
            print "[+] Success!"
            print CLEAR
            break
        except errors.MasterPasswordIncorrect:
            print CLEAR
            print "[-] Password was incorrect."

    main_menu()
    raise NotImplementedError()
    pyvault.save()


if __name__ == '__main__':
    unlock_menu()
    print "\Quitting..."
