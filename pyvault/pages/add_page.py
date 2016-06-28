
# standard
import Tkinter as Tk

# project
from pyvault import constants
from pyvault.pages import page

class AddEntry(page.AbstractPage):

    def start(self):
        self.main.pack()
        # self.clear()

    def _setup(self):
        # title
        self.title = Tk.Message(self.main, text="Add Password", font="TkDefaultFont 16", width=200)
        self.title.pack()

        self._setup_fields()
        self._setup_storage()
        self._setup_master_key_entry()
        self._setup_buttons()

    def _setup_fields(self):
        # fields
        self.frame_fields = Tk.Frame(self.main)
        self.frame_fields.pack()

        self.label_service = Tk.Label(self.frame_fields, text="Service:")
        self.label_service.grid(column=0, row=0, sticky=Tk.E)
        self.entry_service = Tk.Entry(self.frame_fields)
        self.entry_service.grid(column=1, row=0)

        self.label_account = Tk.Label(self.frame_fields, text="Account:")
        self.label_account.grid(column=0, row=1, sticky=Tk.E)
        self.entry_account = Tk.Entry(self.frame_fields)
        self.entry_account.grid(column=1, row=1)

        self.message_warning = Tk.Message(
            self.frame_fields,
            text="Warning: that service/account pair already exists.",
            width=200,
            fg="red",
        )
        self.message_warning.grid(column=2, row=0, columnspan=2, rowspan=2)

        self.label_notes = Tk.Label(self.frame_fields, text="Notes:")
        self.label_notes.grid(column=0, row=2, sticky=Tk.E)
        self.text_notes = Tk.Text(self.frame_fields, width=40, height=3, relief="ridge", borderwidth=4)
        self.text_notes.grid(column=1, row=2, columnspan=3, rowspan=2, sticky=constants.FILLCELL)

    def _setup_storage(self):
        # storage options
        self.labelframe_storage = Tk.LabelFrame(self.main, text="Storage Options")
        self.labelframe_storage.pack()

        self.var_storage = Tk.IntVar()
        self.var_storage.set(1)
        self.radio_store = Tk.Radiobutton(
            self.labelframe_storage,
            text='',
            # text="Store password (AES)",
            variable=self.var_storage,
            value=1)
        self.radio_store.grid(row=0, column=0)
        self.label_store = Tk.Label(self.labelframe_storage, text="Store password with master key (AES)")
        self.label_store.grid(row=0, column=1, columnspan=3, sticky=Tk.W)

        self.label_password = Tk.Label(self.labelframe_storage, text="Password to store:")
        self.label_password.grid(row=1, column=1, sticky=Tk.E)
        self.entry_password = Tk.Entry(self.labelframe_storage, show=constants.HIDDEN)
        self.entry_password.grid(row=1, column=2, sticky=Tk.W)

        self.label_password_repeat = Tk.Label(self.labelframe_storage, text="(Repeat):")
        self.label_password_repeat.grid(row=2, column=1, sticky=Tk.E)
        self.entry_password_repeat = Tk.Entry(self.labelframe_storage, show=constants.HIDDEN)
        self.entry_password_repeat.grid(row=2, column=2, sticky=Tk.W)


        self.radio_derive = Tk.Radiobutton(
            self.labelframe_storage,
            text='',
            # text="Derive password (PBKDF2)",
            variable=self.var_storage,
            value=2)
        self.radio_derive.grid(row=4, column=0)
        self.label_derive = Tk.Label(self.labelframe_storage, text="Derive password from memorized key (PBKDF2)")
        self.label_derive.grid(row=4, column=1, columnspan=3, sticky=Tk.W)

        self.label_key = Tk.Label(self.labelframe_storage, text="Key:")
        self.label_key.grid(row=5, column=1, sticky=Tk.E)
        self.entry_key = Tk.Entry(self.labelframe_storage, show=constants.HIDDEN)
        self.entry_key.grid(row=5, column=2, sticky=Tk.W)

        self.label_key_repeat = Tk.Label(self.labelframe_storage, text="(Repeat):")
        self.label_key_repeat.grid(row=6, column=1, sticky=Tk.E)
        self.entry_key_repeat = Tk.Entry(self.labelframe_storage, show=constants.HIDDEN)
        self.entry_key_repeat.grid(row=6, column=2, sticky=Tk.W)

    def _setup_master_key_entry(self):
        # master key entry
        self.frame_master_key = Tk.Frame(self.main)
        self.frame_master_key.pack()

        self.label_master_key = Tk.Label(self.frame_master_key, text="Master key:")
        self.label_master_key.grid(row=0, column=0, sticky=Tk.E)
        self.entry_master_key = Tk.Entry(self.frame_master_key, show=constants.HIDDEN)
        self.entry_master_key.grid(row=0, column=1, sticky=Tk.W)

    ########################################
    # buttons and actions
    def _setup_buttons(self):
        # buttons
        self.frame_buttons = Tk.Frame(self.main)
        self.frame_buttons.pack()

        self.button = Tk.Button(self.frame_buttons, text="Cancel", command=self.cancel)
        self.button.grid(row=0, column=0, sticky=constants.FILLCELL)

        self.button = Tk.Button(self.frame_buttons, text="OK", command=self.ok)
        self.button.grid(row=0, column=1, sticky=constants.FILLCELL)

    def cancel(self):
        self.add_to_main()

    def ok(self):
        pass

    ########################################
    # transitions
    def add_to_main(self):
        self.transition(constants.MAIN)
