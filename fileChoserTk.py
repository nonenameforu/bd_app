import tkinter as tk
from tkinter import filedialog

class FileChooserButton(tk.Frame):
    def __init__(self, master, button_text="Выбрать файл", **kwargs):
        super().__init__(master, **kwargs)
        
        self.filename = tk.StringVar()
        
        self.button = tk.Button(self, text=button_text, command=self.choose_file)
        self.button.pack()
        
        self.label = tk.Label(self, textvariable=self.filename, width=40, anchor="w", padx=5)
        self.label.pack()

    def choose_file(self):
        filetypes = (("Изображения", "*.png"),)
        filename = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=filetypes
        )
        if filename:
            self.filename.set(filename)

    def get(self):
        return self.filename.get()