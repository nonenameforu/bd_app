
import tkinter as tk
from tkinter import ttk
from table import Table

class uiTable:
    def __init__(self,basetable:Table,tree:ttk.Treeview,tab:ttk.Frame) -> None:
        self.tab = tab
        self.baseTable = basetable
        self.tree = tree