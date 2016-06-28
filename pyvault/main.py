"""
PyVault:  the secure password manager.  Version 5.
"""

# standard
import Tkinter as Tk

# project
from pyvault import constants
from pyvault import shared
from pyvault.pages import add_page
from pyvault.pages import login_page
from pyvault.pages import main_page


def setup():
    """
    Crucial function for creating pages and
    allowing inter-page transitions.
    """

    # create = creation_mage.CreationPage(shared.ROOT)
    login = login_page.LoginPage(shared.ROOT)
    main = main_page.MainPage(shared.ROOT)
    add = add_page.AddEntry(shared.ROOT)

    shared.PAGES[constants.LOGIN] = login
    shared.PAGES[constants.MAIN] = main
    shared.PAGES[constants.ADD] = add


def run_tkinter():
    """Runs the Tkinter app."""
    shared.ROOT.wm_title(constants.TITLE)
    shared.ROOT.mainloop()
    try:
        shared.ROOT.destroy()  # optional?
    except Tk._tkinter.TclError:
        pass


def main():
    """Sets up the app and runs it."""
    setup()
    shared.PAGES[constants.LOGIN].start()

    run_tkinter()

if __name__ == '__main__':
    main()
