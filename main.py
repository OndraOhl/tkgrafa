#!/usr/bin/env python3

from os.path import basename, splitext
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pylab as pl
import os.path
from tkinter import OptionMenu
from scipy.interpolate import CubicSpline
from scipy.interpolate import Akima1DInterpolator
from scipy.interpolate import PchipInterpolator
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
    name = "Foo"
    colors= ['black', 'red', 'green', 'blue', 'magenta', 'purple', 'coral', 'darkgreen']

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)
        self.bind("<Escape>", self.quit)
        self.lbl = tk.Label(self, text="tkGraf")
        self.lbl.pack()


        self.fileFrame = tk.LabelFrame(self, text='Soubor')
        self.fileFrame.pack(padx=5, pady=5, fill='both')
        self.fileEntry = MyEntry(self.fileFrame)
        self.fileEntry.pack(anchor='w', fill='both')
        self.fileBtn = tk.Button(self.fileFrame, text='...', command=self.selectFile)
        self.fileBtn.pack(anchor='e')

        self.dataformatVar = tk.StringVar(value='ROW')
        self.rowRadio = tk.Radiobutton(self.fileFrame, text = 'Data v řádcích', variable = self.dataformatVar, value='ROW')
        self.rowRadio.pack(anchor='w')
        self.columnRadion = tk.Radiobutton(self.fileFrame, text = 'Data ve sloupcích', variable=self.dataformatVar, value='COLUMN')
        self.columnRadion.pack(anchor='w')


        self.grafFrame = tk.LabelFrame(self, text= 'Graf')
        self.grafFrame.pack(padx=5, pady=5, fill='x')


        tk.Label(self.grafFrame, text='Titulek').grid(row=0, column=0)
        self.titleEntry = MyEntry(self.grafFrame)
        self.titleEntry.grid(row=0, column=1, sticky=tk.EW, columnspan=2)


        tk.Label(self.grafFrame, text='Osa X').grid(row=1, column=0)
        self.xEntry = MyEntry(self.grafFrame)
        self.xEntry.grid(row=1, column=1, sticky=tk.EW, columnspan=2)


        tk.Label(self.grafFrame, text='Osa Y').grid(row=2, column=0)
        self.yEntry = MyEntry(self.grafFrame)
        self.yEntry.grid(row=2, column=1, sticky=tk.EW, columnspan=2)


        tk.Label(self.grafFrame, text='Mřížka').grid(row=3, column=0)
        self.gridVar = tk.BooleanVar(value=True)
        self.gridCheck = tk.Checkbutton(self.grafFrame, variable=self.gridVar)
        self.gridCheck.grid(row=3, column=1, sticky='w')


        self.lineVar = tk.StringVar(value='--')
        tk.Label(self.grafFrame, text='čára').grid(row=4, column=0)
        self.lineCBox = tk.OptionMenu(self.grafFrame, self.lineVar, 'none', '-', '--', '-.', ':')
        self.lineCBox.grid(row=4, column=1, sticky='w')
        self.colorVar = tk.StringVar(value="Black")
        tk.OptionMenu(self.grafFrame, self.colorVar,*self.colors).grid(row=4, column=2, sticky='w')
        

        self.markerVar = tk.StringVar(value='x')
        tk.Label(self.grafFrame, text='marker').grid(row=5, column=0)
        tk.OptionMenu(self.grafFrame, self.markerVar, 'none', *tuple('xX+P,.o*1234')).grid(row=5, column=1, sticky='w')
        self.mcolorVar = tk.StringVar(value="Black")
        tk.OptionMenu(self.grafFrame, self.mcolorVar,*self.colors).grid(row=5, column=2, sticky='w')
        

        self.interpolVar = tk.StringVar(value='None')
        tk.Label(self.grafFrame, text='interpolace').grid(row=6, column=0)
        tk.OptionMenu(self.grafFrame, self.interpolVar, 'none', 'CubicSpline', 'PchinInterpolator','Akima1DInterpolator').grid(row=6, column=1, sticky='w')
        self.icolorVar = tk.StringVar(value="Black")
        tk.OptionMenu(self.grafFrame, self.icolorVar,*self.colors).grid(row=6, column=2, sticky='w')


        tk.Button(self, text='Vykreslit', command=self.plot).pack(anchor='w')


        self.btn = tk.Button(self, text="Quit", command=self.quit)
        self.btn.pack(anchor='e')


        #hlavni menu
        self.mainMenu = tk.Menu(self)

        #file menu
        fileMenu=tk.Menu(self.mainMenu)
        fileMenu.add_command(label='Open', command=self.quit)
        fileMenu.add_command(label='Save', command=self.quit)
        fileMenu.add_separator()
        fileMenu.add_command(label='Quit', command=self.quit)
        self.mainMenu.add_cascade(label='File', menu=fileMenu)

        #edit menu
        editMenu=tk.Menu(self.mainMenu)
        ovoceMenu=tk.Menu(editMenu)
        zeleninaMenu=tk.Menu(editMenu)
        editMenu.add_cascade(label='ovoce', menu=ovoceMenu)
        editMenu.add_cascade(label='zelenina', menu=zeleninaMenu)

        ovoceMenu.add_command(label='jablko', command=self.quit)
        ovoceMenu.add_command(label='hruška')
        ovoceMenu.add_command(label='svěstka')

        zeleninaMenu.add_radiobutton(label='zeli')
        zeleninaMenu.add_radiobutton(label='kapusta')
        zeleninaMenu.add_radiobutton(label='mrkev')



        self.mainMenu.add_cascade(label='Edit', menu=editMenu)




        self.mainMenu.add_cascade(label='Selection')

        self.config(menu=self.mainMenu)
        self.bind('<3>', self.showmenu)



    def showmenu(self, event: tk.Event):
        self.mainMenu.post(event.x_root, event.y_root)


    def selectFile(self):
        self.fileEntry.value = filedialog.askopenfilename()
        self.fileEntry.xview_moveto(1)

    def plot(self):
        if not os.path.isfile(self.fileEntry.value):
            return
        with open(self.fileEntry.value, 'r') as f:
            if self.dataformatVar.get() == 'ROW':
                x = f.readline().split(';')
                x = [float(i.replace(',','.')) for i in x]
                y = f.readline().split(';')
                y = [float(i.replace(',','.')) for i in y]
            elif self.dataformatVar.get() == 'COLUMN':
                x = []
                y = []
                while True:
                    line = f.readline()
                    if line == '':
                        break
                    if ';' not in line:
                        continue
                    x1, y1 = line.split(';')
                    x.append(float(x1.replace(','),('.')))
                    y.append(float(y1.replace(','),('.')))


        


        
        pl.plot(x,
                y, 
                linestyle = self.lineVar.get(),
                marker=self.markerVar.get(), 
                color= self.colorVar.get(),
                markerfacecolor = self.mcolorVar.get(),
                markeredgecolor = self.mcolorVar.get()
                )
        
        interpolace = {}
        interpolace['CubicSpline'] = CubicSpline
        interpolace['PchipInterpolator'] = PchipInterpolator
        interpolace['Akima1DInterpolator'] = Akima1DInterpolator


        


        if self.interpolVar.get() in interpolace:
            min_x = min(x)
            max_x = max(x)
            spl = interpolace[self.interpolVar.get()](x,y)
            new_x = pl.linspace(min_x, max_x, 777)
            new_y = spl(new_x)
            pl.plot(new_x, new_y, color=self.icolorVar.get())

        pl.title(self.titleEntry.value)
        pl.xlabel(self.xEntry.value)
        pl.ylabel(self.yEntry.value)
        pl.grid(self.gridVar.get())
        pl.show()
    
    def quit(self, event=None):
        super().quit()


app = Application()
app.mainloop()