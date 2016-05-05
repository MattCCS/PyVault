"""
This file contains the abstract page implementation.
"""

# standard
import abc
import Tkinter as Tk
# import ttk as Tk

# project
import shared


class AbstractPage(object):
    """Abstract page implementation."""

    __metaclass__ = abc.ABCMeta

    def __init__(self, pages):
        self.__pages = pages
        self.root = Tk.Frame(shared.ROOT)
        self._setup()

    @abc.abstractmethod
    def start(self):
        pass

    def _end(self):
        self.root.pack_forget()

    def transition(self, page):
        self._end()
        self.__pages[page].start()
