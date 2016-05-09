"""
Secure password manager, version 5.
"""

# standard
import Tkinter as Tk

# project
import add_entry
import constants
import shared
import login_page
import main_page


def setup():
    """
    Crucial function for creating pages and
    allowing inter-page transitions.
    """

    login = login_page.LoginPage(shared.ROOT)
    main = main_page.MainPage(shared.ROOT)
    add = add_entry.AddEntry(shared.ROOT)

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
