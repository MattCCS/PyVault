"""
This file contains the abstract page implementation.
"""

# standard
import abc
import Tkinter as Tk

# project
import shared


class AbstractPage(object):
    """Abstract page implementation."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, root):
        self.root = root
        self.main = Tk.Frame(root)
        self._setup()

    @abc.abstractmethod
    def start(self):
        pass

    def _end(self):
        self.main.pack_forget()

    def transition(self, page):
        self._end()
        shared.PAGES[page].start()


# class FocusPage(AbstractPage):

#     def _end(self):
#         AbstractPage._end(self)
#         self.root.grab_release()


# def make_focus_root(old_root):
#     old_root.configure(state="disable")
#     root = Tk.Toplevel()
#     root.grab_set()
#     root.wm_attributes('-topmost', 1)
#     return root
