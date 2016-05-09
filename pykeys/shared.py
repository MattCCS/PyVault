"""
This file contains data which is shared across the entire program.
"""

# standard
import Tkinter as Tk
# import ttk as Tk

# project
from pykeys import constants

# data
PAGES = {}

# app
ROOT = Tk.Tk()
ROOT.minsize(constants.MIN_WIDTH, constants.MIN_HEIGHT)
ROOT.geometry("{}x{}".format(constants.START_WIDTH, constants.START_HEIGHT))
