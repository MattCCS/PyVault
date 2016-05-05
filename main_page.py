"""
This file contains the class which runs the main page.
"""

# standard
import Tkinter as Tk
# import ttk as Tk

# project
import constants
import page
import shared


class MainPage(page.AbstractPage):
    """This class forms and interacts with the main page."""

    def start(self):
        """Creates the main window."""
        self.root.pack(fill="both", expand="yes")

    def _setup(self):
        """Sets up this page -- only call once!"""
        self.main_frame = Tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand="yes")

        # back button
        self.back = Tk.Button(
            self.main_frame,
            text="Back to login",
            command=self.main_to_login
        )
        self.test = Tk.Label(self.main_frame, text="Just a test!")

        self.back.grid(row=0, column=0)
        self.test.grid(row=1, column=1)

    def main_to_login(self):
        shared.MASTER_PASSWORD = None
        self.transition(constants.LOGIN)
