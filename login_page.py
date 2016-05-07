"""
This file contains the class which runs the login page.
"""

# standard
import Tkinter as Tk
# import ttk as Tk

# project
import constants
import page
import shared


class LoginPage(page.AbstractPage):
    """This class forms and interacts with the login page."""

    def start(self):
        """Creates the login window."""
        self.root.pack(fill="both", expand="yes")
        self.err_var.set('')
        self.pw_entry.delete(0, 'end')  # http://stackoverflow.com/questions/2260235/how-to-clear-the-entry-widget-after-a-button-is-pressed-in-tkinter

    def _setup(self):
        """Sets up this page -- only call once!"""
        # make the outermost frame
        # self.login_frame = Tk.LabelFrame(self.root, text="Secure Password Manager", borderwidth=2)
        self.login_frame = Tk.Frame(self.root)
        # self.login_frame.pack(fill="both", expand="yes")
        # self.login_frame.pack(fill="both")
        self.login_frame.pack(expand="yes")
        # self.login_frame.pack()

        self._lock = Tk.PhotoImage(file="lock-128.gif")
        _border = 0
        _canv = Tk.Canvas(
            self.login_frame,
            width=128 - 36,
            height=128,
            borderwidth=_border,
            relief="raised"
        )
        _canv.pack()
        _dim = 64 + 3 + _border
        _canv.create_image(_dim - 36 / 2, _dim, image=self._lock)

        _expln = Tk.StringVar()
        _expln.set("The password table is encrypted.\nTo decrypt it, please enter the master password below.")
        self.table_pw_expln = Tk.Message(
            self.login_frame,
            textvariable=_expln,
            width=constants.MIN_WIDTH - 20,
            justify=Tk.CENTER,
            pady=20
        )
        self.table_pw_expln.pack()

        # password entry widgets
        self.pw_grid = Tk.Frame(self.login_frame)
        self.pw_grid.pack()

        # label and entry field
        self.pw_label = Tk.Label(self.pw_grid, text="Password:")
        self.table_pw_var = Tk.StringVar()
        self.pw_entry = Tk.Entry(
            self.pw_grid,
            show="*",
            textvariable=self.table_pw_var
        )
        self.pw_entry.bind("<Return>", lambda k: self.table_pw_enter())

        # error message
        self.err_var = Tk.StringVar()
        self.err_var.set('')
        self.err_message = Tk.Message(
            self.pw_grid,
            textvariable=self.err_var,
            width=constants.MIN_WIDTH - 20,
            justify=Tk.CENTER,
            fg="red"
        )

        self.pw_label.grid(row=0, column=0)
        self.pw_entry.grid(row=0, column=1)
        self.err_message.grid(row=1, column=0, columnspan=2)

    def table_pw_enter(self):
        table_password = self.table_pw_var.get()

        # TODO: actually do symmetric crypto
        if table_password == 'trustno1' or not table_password:
            shared.MASTER_PASSWORD = table_password
            self.login_to_main()
        else:
            self.err_var.set("Master password was incorrect.")

    def login_to_main(self):
        self.transition(constants.MAIN)
