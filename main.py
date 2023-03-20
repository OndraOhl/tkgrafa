#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pylab as pl

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if not "textvariable" in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class Application(tk.Tk):
    name = basename(splitext(basename(__file__.capitalize()))[0])
    name = "GRAFY"

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="tkGraf")
        self.lbl.pack()

        self.fileFrame = tk.LabelFrame(self, text="Soubor")
        self.fileFrame.pack(padx=5, pady=5, fill='x')
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(anchor='w', fill='x')
        self.fileBtn = tk.Button(self.fileFrame, text="...", command=self.selectFile)
        self.fileBtn.pack(anchor="e")

        self.dataformatVar = tk.StringVar(value='ROW')
        self.rowRadio = tk.Radiobutton(
            self.fileFrame, text="Dada v řádcích", variable=self.dataformatVar, value='ROW'
        )
        self.rowRadio.pack(anchor='w')
        self.columnRadio = tk.Radiobutton(
            self.fileFrame,
            text="Data ve sloupcích",
            variable=self.dataformatVar,
            value='COLUMN',
        )
        self.columnRadio.pack(anchor='w')


        self.grafFrame = tk.LabelFrame(self, text='Graf')
        self.grafFrame.pack(padx=5, pady=5, anchor='w', fill='x')
        
        tk.Label(self.grafFrame, text='Titulek').grid(row=0, column=0)
        self.titleEntry = MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0, column=1, sticky=tk.EW)
        tk.Label(self.grafFrame, text='osa X').grid(row=1, column=0)
        self.xEntry = MyEntry(self.grafFrame)
        self.xEntry.grid(row=1, column=1, columnspan=2, sticky=tk.EW)
        tk.Label(self.grafFrame, text='osa Y').grid(row=2, column=0)
        self.yEntry = MyEntry(self.grafFrame)
        self.yEntry.grid(row=2, column=1, sticky=tk.EW)
        tk.Label(self.grafFrame, text='mřížka').grid(row=3, column=0)
        self.gridCheck = tk.Checkbutton(self.grafFrame)
        self.gridCheck.grid(row=3, column=1, sticky='w')
        
        self.lineVar = tk.StringVar()
        tk.Label(self.grafFrame, text='čára').grid(row=4, column=0)
        self.lineCBox = tk.OptionMenu(self.grafFrame, self.lineVar, '-', '--', '-.', ':')
        self.lineCBox.grid(row=4, column=1, sticky='w')
        

        tk.Button(self, text="Vykreslit", command=self.plot).pack(anchor='w')

        tk.Button(self, text="Quit", command=self.quit).pack(anchor='e')

    def selectFile(self):
        self.fileEntry.value = filedialog.askopenfilename()

    def plot(self):
        with open(self.fileEntry.value, 'r') as f:
            x = f.readline().split(';')
            y = f.readline().split(';')
            x = [float(i.replace(',',".")) for i in x]
            y = [float(i.replace(',',".")) for i in y]
        pl.plot(x,y)
        pl.show()

    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()
