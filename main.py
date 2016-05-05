"""
Secure password manager, version 5.
"""

# standard
import Tkinter as Tk
import ttk

# project
import constants


class PWMApp(object):

    def __init__(self, root):

        self._root = root
        self.root = Tk.Frame(self._root)
        self.root.pack(fill="both", expand="yes")
        self.master_password = None

        self.login_create()

    def login_create(self):
        """Creates the login window."""

        # make the outermost frame
        # self.login_frame = Tk.LabelFrame(self.root, text="Secure Password Manager", borderwidth=2)
        self.login_frame = Tk.Frame(self.root)
        # self.login_frame.pack(fill="both", expand="yes")
        # self.login_frame.pack(fill="both")
        self.login_frame.pack(expand="yes")
        # self.login_frame.pack()

        self._lock = Tk.PhotoImage(file="lock-128.gif")
        _border = 0
        _canv = Tk.Canvas(self.login_frame, width=128 - 36, height=128, borderwidth=_border, relief="raised")
        _canv.pack()
        _dim = 64 + 3 + _border
        _canv.create_image(_dim - 36 / 2, _dim, image=self._lock)

        _expln = Tk.StringVar()
        _expln.set("The password table is encrypted.\nTo decrypt it, please enter the master password below.")
        self.table_pw_expln = Tk.Message(self.login_frame, textvariable=_expln, width=constants.MIN_WIDTH-20, justify=Tk.CENTER, pady=20)
        self.table_pw_expln.pack()

        # password entry widgets
        self.pw_grid = Tk.Frame(self.login_frame)
        self.pw_grid.pack()

        # label and entry field
        self.pw_label = Tk.Label(self.pw_grid, text="Password:")
        self.table_pw_var = Tk.StringVar()
        self.pw_entry = Tk.Entry(self.pw_grid, show="*", textvariable=self.table_pw_var)
        self.pw_entry.bind("<Return>", lambda k: self.table_pw_enter())

        # attempt reminder
        # ...

        # error message
        self.err_var = Tk.StringVar()
        self.err_var.set('')
        self.err_message = Tk.Message(self.pw_grid, textvariable=self.err_var, width=constants.MIN_WIDTH-20, justify=Tk.CENTER, fg="red")

        self.pw_label.grid(row=0, column=0)
        self.pw_entry.grid(row=0, column=1)
        self.err_message.grid(row=1, column=0, columnspan=2)

    def table_pw_enter(self):
        table_password = self.table_pw_var.get()
        print repr(table_password)
        if table_password == 'trustno1' or not table_password:
            print "OK"
            self.master_password = table_password
            self.login_to_main()
        else:
            print "BAD"
            self.err_var.set("Table password was incorrect.")

    def login_to_main(self):
        self.login_frame.pack_forget()
        self.main_create()

    ########################################

    def main_create(self):
        """Creates the main window."""
        self.main_frame = Tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand="yes")

        self.back = Tk.Button(self.main_frame, text="Back to login", command=self.main_to_login)
        self.test = Tk.Label(self.main_frame, text="Just a test!")

        self.back.grid(row=0, column=0)
        self.test.grid(row=1, column=1)

    def main_to_login(self):
        self.main_frame.pack_forget()
        self.master_password = None
        self.login_create()


ROOT = Tk.Tk()
ROOT.minsize(constants.MIN_WIDTH, constants.MIN_HEIGHT)
ROOT.geometry("{}x{}".format(constants.START_WIDTH, constants.START_HEIGHT))
# ROOT.geometry("480x320")
# ROOT.lift()

APP = PWMApp(ROOT)

# pop_to_front(ROOT)
ROOT.mainloop()
try:
    ROOT.destroy()  # optional; see description below
except Tk._tkinter.TclError:
    pass
