"""
This file contains the class which runs the main page.
"""

# standard
import base64
import os
import Tkinter as Tk

# project
import add_entry
import constants
import copy_paste
import page
import shared
import passwords

def set_readonly_label(entry, text):
    entry.configure(state="normal")
    entry.delete(0, 'end')
    entry.insert(0, text)
    entry.configure(state="readonly")


class MainPage(page.AbstractPage):
    """This class forms and interacts with the main page."""

    def start(self):
        """Creates the main window."""
        self.main.pack(fill="both", expand="yes")

    def _setup(self):
        """Sets up this page -- only call once!"""

        self._setup_navigation()
        self._setup_database()
        self._setup_generator()

    def _setup_navigation(self):

        ########################################
        # navigation
        self.frame_navigation = Tk.Frame(self.main)
        self.frame_navigation.pack(anchor=Tk.W)

        # self.listbox_keys = Tk.Listbox(self.main, relief="ridge", borderwidth=4)
        # self.listbox_keys.insert(Tk.END, "test")
        # self.listbox_keys.pack(expand="yes", fill="x")

        # buttons
        self.button_back = Tk.Button(
            self.frame_navigation,
            text="Back to login",
            command=self.main_to_login
        )
        self.button_change = Tk.Button(
            self.frame_navigation,
            text="Change Master Password",
        )
        self.entry_search = Tk.Entry(self.frame_navigation)
        # self.label_test = Tk.Label(self.main_frame, text="Just a test!")


        self.button_back.grid(row=0, column=0)
        self.button_change.grid(row=0, column=1)
        self.entry_search.grid(row=1, column=0, columnspan=2, sticky=Tk.W)

    def _setup_database(self):

        ########################################
        # keychain
        self.frame_database = Tk.Frame(self.main)
        self.frame_database.pack(anchor=Tk.W, fill="both", expand="yes")
        self.frame_database.columnconfigure(0, weight=1)
        self.frame_database.rowconfigure(0, weight=1)

        # notes and buttons
        self.listbox_keys = Tk.Listbox(self.frame_database, relief="ridge", borderwidth=4)
        self.listbox_keys.grid(row=0, column=0, columnspan=2, rowspan=5, sticky=constants.FILLCELL)
        self.text_notes = Tk.Text(self.frame_database, width=20, height=10, relief="ridge", borderwidth=4)
        self.text_notes.grid(row=0, column=2, sticky=constants.FILLCELL)
        self.button_show = Tk.Button(self.frame_database, text="Show", command=self.main_to_show)
        self.button_show.grid(row=1, column=2, sticky=constants.FILLCELL)
        self.button_add = Tk.Button(self.frame_database, text="Add", command=self.main_to_add)
        self.button_add.grid(row=2, column=2, sticky=constants.FILLCELL)
        self.button_edit = Tk.Button(self.frame_database, text="Edit", command=self.main_to_edit)
        self.button_edit.grid(row=3, column=2, sticky=constants.FILLCELL)
        self.button_delete = Tk.Button(self.frame_database, text="Delete", command=self.main_to_delete)
        self.button_delete.grid(row=4, column=2, sticky=constants.FILLCELL)

    def _setup_generator(self):

        ########################################
        # password generator
        self.frame_generator = Tk.LabelFrame(self.main, text="Password Generator")
        self.frame_generator.pack(anchor=Tk.CENTER)

        self.var_uppercase = Tk.BooleanVar()
        self.var_lowercase = Tk.BooleanVar()
        self.var_digits = Tk.BooleanVar()
        self.var_special = Tk.BooleanVar()
        self.var_custom = Tk.BooleanVar()
        self.var_all = Tk.BooleanVar()
        self.var_uppercase.set(True)
        self.var_lowercase.set(True)
        self.var_digits.set(True)
        self.var_special.set(True)
        self.check_uppercase = Tk.Checkbutton(self.frame_generator, text="uppercase (ABC...)", variable=self.var_uppercase)
        self.check_lowercase = Tk.Checkbutton(self.frame_generator, text="lowercase (abc...)", variable=self.var_lowercase)
        self.check_digits = Tk.Checkbutton(self.frame_generator, text="digits (012...)", variable=self.var_digits)
        self.check_special = Tk.Checkbutton(self.frame_generator, text="punctuation ([]!@#...)", variable=self.var_special)
        self.check_custom = Tk.Checkbutton(self.frame_generator, text="custom", variable=self.var_custom)
        self.entry_custom = Tk.Entry(self.frame_generator, width=12)
        self.check_all = Tk.Checkbutton(self.frame_generator, text="*ALL* (overrides others)", variable=self.var_all)

        max_password_length = 64
        self.label_password_length = Tk.Label(self.frame_generator, text="Password length")
        self.var_password_length = Tk.IntVar()
        self.var_password_length.set(16)
        self.scale_password_length = Tk.Scale(
            self.frame_generator,
            orient="horizontal",
            from_=10,
            to=max_password_length,
            variable=self.var_password_length,
            command=lambda k: self.generate_password(),
        )

        self.entry_password = Tk.Entry(self.frame_generator, width=max_password_length)
        self.entry_password.configure(state="readonly")

        # self.var_radio = Tk.IntVar()
        # self.var_radio.set(1)
        self.label_buttons = Tk.Label(self.frame_generator, text="What to do:")
        # self.radio_show = Tk.Radiobutton(self.frame_generator, text="Show", variable=self.var_radio, value=1)
        # self.radio_copy = Tk.Radiobutton(self.frame_generator, text="Copy to clipboard", variable=self.var_radio, value=2)
        self.button_preview = Tk.Button(
            self.frame_generator,
            text="Preview",
            command=self.generate_password
        )
        self.button_generate_and_copy = Tk.Button(
            self.frame_generator,
            text="Generate and copy to clipboard",
            command=self.generate_and_copy
        )

        # placement
        self.check_uppercase.grid(row=0, column=0, sticky=Tk.W, columnspan=2)
        self.check_lowercase.grid(row=1, column=0, sticky=Tk.W, columnspan=2)
        self.check_digits.grid(row=2, column=0, sticky=Tk.W, columnspan=2)

        self.check_special.grid(row=0, column=1, sticky=Tk.W, columnspan=2)
        self.check_custom.grid(row=1, column=1, sticky=Tk.W, columnspan=1)
        self.entry_custom.grid(row=1, column=2, columnspan=2, sticky=constants.FILLCELL)
        self.check_all.grid(row=2, column=1, sticky=Tk.W, columnspan=2)

        self.label_password_length.grid(row=3, column=0, sticky=Tk.S)
        self.scale_password_length.grid(row=3, column=1, columnspan=3, sticky=constants.FILLCELL)

        self.entry_password.grid(row=4, column=0, columnspan=4, sticky=constants.FILLCELL)

        self.label_buttons.grid(row=5, column=0)
        # self.radio_show.grid(row=5, column=1)
        # self.radio_copy.grid(row=5, column=2)
        self.button_preview.grid(row=5, column=1, sticky=constants.FILLCELL)
        self.button_generate_and_copy.grid(row=5, column=2, columnspan=2, sticky=constants.FILLCELL)

    def generate_password(self, show=True):
        password = os.urandom(10)
        password = base64.b64encode(password)

        upper = self.var_uppercase.get()
        lower = self.var_lowercase.get()
        digits = self.var_digits.get()
        special = self.var_special.get()
        custom = set(self.entry_custom.get()) if self.var_custom.get() else set()
        all_chars = self.var_all.get()
        length = self.var_password_length.get()

        if all_chars:
            chars = passwords.ALL
        else:
            chars = passwords.password_chars(
                upper=upper,
                lower=lower,
                digits=digits,
                special=special,
                custom=custom
            )

        if not chars:
            return  # don't change the display

        password = passwords.generate_password(chars=chars, length=length)

        if show:
            set_readonly_label(self.entry_password, password)

        return password

    def generate_and_copy(self):
        password = self.generate_password(show=False)
        copy_paste.write_to_clipboard(password)

    ########################################
    # transitions

    def main_to_show(self):
        pass

    def main_to_add(self):
        self.transition(constants.ADD)

    def main_to_login(self):
        self.transition(constants.LOGIN)

    def main_to_edit(self):
        pass

    def main_to_delete(self):
        pass
