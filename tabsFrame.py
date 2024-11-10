import tkinter as tk
from tkinter import ttk
from table import Table
from uiTable import uiTable


class Tabs:
    def __init__(self,root) -> None:
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")
        self.allTables = []

        # Создаем вкладки с таблицами
        for i in range(3):
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=f"Вкладка {i+1}")
            
            # Создаем таблицу для каждой вкладки
            tree = ttk.Treeview(tab, columns=("Column 1", "Column 2", "Column 3"), show="headings")
            tree.heading("Column 1", text="Столбец 1")
            tree.heading("Column 2", text="Столбец 2")
            tree.heading("Column 3", text="Столбец 3")
            
            # Добавляем примерные данные
            for j in range(10):
                tree.insert("", "end", values=(f"Значение {j+1}", f"Значение {j+2}", f"Значение {j+3}"))
            
            tree.pack(expand=True, fill="both")

    def addTab(self,tab:Table):
        self.notebook.add(tab, text=f"Вкладка {tab.GetTitel}")
        self.__addTable(tab)


    def __addTable(self,tab:Table):
        tree = ttk.Treeview(tab, columns=("Column 1", "Column 2", "Column 3"), show="headings")
        tab = uiTable(tab,tree)
        self.allTables.append(tab)



    def insertData():
        pass



