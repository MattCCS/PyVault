"""
Secure password manager, version 5.
"""

# standard
import Tkinter as Tk
# import ttk as Tk

# project
import constants
import shared
import login_page
import main_page


def setup():
    """
    Crucial function for creating pages and
    allowing inter-page transitions.
    """
    pages = {}

    login = login_page.LoginPage(pages)
    main = main_page.MainPage(pages)

    pages[constants.LOGIN] = login
    pages[constants.MAIN] = main

    return pages


def run_tkinter():
    """Runs the Tkinter app."""
    shared.ROOT.mainloop()
    try:
        shared.ROOT.destroy()  # optional?
    except Tk._tkinter.TclError:
        pass


def main():
    """Sets up the app and runs it."""
    pages = setup()
    pages[constants.LOGIN].start()

    run_tkinter()

if __name__ == '__main__':
    main()
