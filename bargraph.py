#CODE BY KIAN
from tkinter import *
from numpy import arange, sin
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class b_graph(Tk):
    def __init__(self):
        Tk.__init__(self, None)
        self.frame=Frame(None)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)

        self.frame.grid(row=0,column=0, sticky=W+E+N+S)

        f, ax = plt.subplots()

        data = (21, 41, 35, 67)
        bar_colors = ['skyblue', 'skyblue', 'red', 'red']
        ind = np.arange(4)
        width = .4

        bar1 = ax.bar(ind, data, width, color=bar_colors)

        ax.set_ylabel('Amount')
        ax.set_title('Income Data')
        ax.set_xticks(ind + width / 20)
        ax.set_xticklabels(('Gross\nIncome', 'Net\nIncome', 'Gross\nIncome', 'Net\nIncome'))

        self.hbar=Scrollbar(self.frame,orient=HORIZONTAL)
        self.vbar=Scrollbar(self.frame,orient=VERTICAL)

        self.canvas=FigureCanvasTkAgg(f, master=self.frame)
        self.canvas.get_tk_widget().config(bg='#FFFFFF',scrollregion=(0,0,500,500))
        self.canvas.get_tk_widget().config(width=300,height=300)
        self.canvas.get_tk_widget().config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=W+E+N+S)

        self.hbar.grid(row=1, column=0, sticky=W+E)
        self.hbar.config(command=self.canvas.get_tk_widget().xview)
        self.vbar.grid(row=0, column=1, sticky=N+S)
        self.vbar.config(command=self.canvas.get_tk_widget().yview)

        self.frame.config(width=100, height=100)

if __name__ == '__main__':

    Window = b_graph()
    Window.geometry('600x500')
    Window.title('Income')
    Window.rowconfigure(0, weight=1)
    Window.columnconfigure(0, weight=1)
    Window.mainloop()
