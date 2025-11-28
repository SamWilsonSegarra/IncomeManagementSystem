#Written By: cedrick
from tkinter import *
#import customtkinter
from tkinter.ttk import Combobox
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkcalendar import DateEntry
import datetime
import numpy as np
import matplotlib.figure as mfig

root = Tk()
#MAINWINDOW Details
    #root.grid_propagate(False)
root.geometry("1080x720")
root.minsize(800,600)
ic0n = PhotoImage(file='coin.png')
root.iconphoto(True, ic0n)
root.title("Income Management System")

#SHARED FUNCTIONS, CLASSES, & VARIABLES
varTimeSpan = StringVar()
startDate = StringVar()

def validate_amount(text):
    if text == "":
        return True
    # Accept numbers or decimal numbers
    return text.replace(".", "", 1).isdigit()
vcmd = (root.register(validate_amount), "%P")

def dateSelect(event):
    selected = DateSelct.get()
    startDate.set(selected)
    print("Selected date:", startDate.get())

class ScrollFrame(Frame):
    def __init__(self, container, height=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        if height is not None:
            self.configure(height=height)
            self.pack_propagate(False)
        self.canvas = Canvas(self, highlightthickness=0)
        self.vscroll = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.scrollable_frame = Frame(self.canvas)
        self._window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        def _on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", _on_frame_configure)

        def _on_canvas_configure(event):
            canvas_width = event.width
            self.canvas.itemconfig(self._window_id, width=canvas_width)
        self.canvas.bind("<Configure>", _on_canvas_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vscroll.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")




#MENU FUNCTIONS



#EXPENSE FUNCTIONS
expense_data = []
menu_expEnt = Menu(root, tearoff=0)
menu_expEnt.add_command(label="Delete Entry")
def addExpense():
    parent = ExpScrollFrame.scrollable_frame
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    catExp = Entry(parent, font=("Calibri", 12), relief=SUNKEN, borderwidth=1)
    amtExp = Entry(parent, font=("Calibri", 12), relief=SUNKEN, borderwidth=1,
                   validate='key', validatecommand=vcmd)
    rowexp = len(expense_data)
    catExp.grid(row=rowexp, column=0, sticky="nsew", padx=2, pady=2)
    amtExp.grid(row=rowexp, column=1, sticky="nsew", padx=2, pady=2)
    expEnt_record = {"category": catExp, "amount": amtExp}
    expense_data.append(expEnt_record)
    catExp.bind("<Button-3>", lambda event, rec=expEnt_record: expEnt_menu(event, rec))
    catExp.focus_set()
#amount = float(amount_str) if amount_str else 0 (converting amount_str to float)
def expEnt_menu(event, record):
    menu_expEnt.entryconfigure(0, command=lambda: deleteExp_row(record))
    menu_expEnt.tk_popup(event.x_root, event.y_root)
def deleteExp_row(record):
    record["category"].grid_forget()
    record["amount"].grid_forget()
    expense_data.remove(record)
    for i, rec in enumerate(expense_data):
        rec["category"].grid(row=i, column=0, sticky=NSEW)
        rec["amount"].grid(row=i, column=1, sticky=NSEW)



#INCOME FUNCTIONS
income_data = []
menu_incEnt = Menu(root, tearoff=0)
menu_incEnt.add_command(label="Delete Entry")
def addIncome():
    parent = IncScrollFrame.scrollable_frame
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_columnconfigure(1, weight=1)
    catInc = Entry(parent, font=("Calibri", 12), relief=SUNKEN, borderwidth=1)
    amtInc = Entry(parent, font=("Calibri", 12), relief=SUNKEN, borderwidth=1,
                   validate='key', validatecommand=vcmd)
    rowinc = len(income_data)
    catInc.grid(row=rowinc, column=0, sticky="nsew", padx=2, pady=2)
    amtInc.grid(row=rowinc, column=1, sticky="nsew", padx=2, pady=2)
    incEnt_record = {"category": catInc, "amount": amtInc}
    income_data.append(incEnt_record)
    catInc.bind("<Button-3>", lambda event, rec=incEnt_record: incEnt_menu(event, rec))
    catInc.focus_set()
#amount = float(amount_str) if amount_str else 0 (converting amount_str to float)
def incEnt_menu(event, record):
    menu_incEnt.entryconfigure(0, command=lambda: deleteInc_row(record))
    menu_incEnt.tk_popup(event.x_root, event.y_root)
def deleteInc_row(record):
    record["category"].grid_forget()
    record["amount"].grid_forget()
    income_data.remove(record)
    for i, rec in enumerate(income_data):
        rec["category"].grid(row=i, column=0, sticky=NSEW)
        rec["amount"].grid(row=i, column=1, sticky=NSEW)



#COMPARISON(LINE-CHART) FUNCTIONS
#def lineGraph():
    #body

#Main Menu
Menubar = Menu(root, relief=RAISED, borderwidth=1)
root.config(menu=Menubar)
fileMenu = Menu(Menubar, tearoff=0)
Menubar.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Open", command='doNothing')
fileMenu.add_command(label="Save", command='doNothing')
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.quit)

#Title-Bar Frame
Titlebar = Frame(root)
Titlebar.place(x=0,y=0,relwidth=1,h=35)
SysTitle = Label(Titlebar,
               text="Income Management System",
               font=("Calibri", 25, "bold"),
               fg="black",
               padx=5,pady=5,
               compound='bottom').pack(side=TOP,fill=X)
#MAIN FRAME
mainFrame = Frame(root)
mainFrame.place(x=0,y=35,relwidth=1,relh=1,anchor=NW)
mainFrame.grid_columnconfigure((0, 1, 2), weight=1)
mainFrame.grid_rowconfigure(0, weight=1)
    #3 Sub-Frames + next&prev buttons frame
ExpFrame = Frame(mainFrame,bg="lightblue")
IncFrame = Frame(mainFrame,bg="lightgreen")
LineFrame = Frame(mainFrame,bg="lightcoral")
DateRel = Frame(ExpFrame,bg="gray")
NextPrev = Frame(IncFrame,bg="green")
ExpFrame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
ExpFrame.grid_columnconfigure((0, 1), weight=1)
IncFrame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
IncFrame.grid_columnconfigure((0, 1), weight=1)
LineFrame.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
LineFrame.grid_columnconfigure((0, 1), weight=1)
DateRel.grid(row=2,column=0,columnspan=2,padx=4,pady=4,sticky=S)
DateRel.grid_rowconfigure(0,weight=1)
NextPrev.grid(row=2,column=0,columnspan=2,sticky=S)
NextPrev.grid_rowconfigure(0,weight=1)

#Expense Frame Widgets
LabelEx1 = Label(ExpFrame,text='Expenses:',font=("Calibri", 14))
CanvChartExp = Canvas(ExpFrame,bg='pink')
ExpListCont = Frame(ExpFrame, bg="yellow", width=200, height=150, relief=SUNKEN, borderwidth=2)
ExpScrollFrame = ScrollFrame(ExpListCont, height=150)
totExp = Label(ExpListCont,text='Total Expenses: ',font=("Calibri", 14))
addExp = Button(ExpFrame,text='Add Expense',font=("Calibri", 14), command=addExpense)
chartE = Button(ExpFrame,text='Generate Chart',font=("Calibri", 14))
LabelEx1.grid(row=0,column=0,sticky=N)
CanvChartExp.grid(row=1,column=0,columnspan=2,padx=10,pady=10,sticky=NSEW)
ExpListCont.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
ExpListCont.grid_propagate(False)
ExpScrollFrame.pack(fill="both", expand=True)
totExp.pack(fill="both", expand=True)
addExp.grid(row=4,column=0,padx=5,pady=5,sticky=NSEW)
chartE.grid(row=4,column=1,padx=5,pady=5,sticky=NSEW)

#Date Related Elements
DateSelct  = DateEntry(DateRel,font=('Arial',12),selectmode='day',year=2025,month=11,day=22)
TimeSpanSel = Combobox(DateRel,font=('Arial',12),
                      textvariable=varTimeSpan,
                      values=['Weeks','Months','Years'],
                      state='readonly')
varTimeSpan.set("Weeks")
TimeSpanSel.bind("<<ComboboxSelected>>")
DateSelct.bind("<<DateEntrySelected>>", dateSelect)
DateSelct.pack(side=LEFT)
TimeSpanSel.pack(side=LEFT)

#Income Frame Widgets
LabelIn1 = Label(IncFrame,text='Income Source(s):',font=("Calibri", 14))
CanvChartInc = Canvas(IncFrame,bg='pink')
IncListCont = Frame(IncFrame, bg="yellow", width=200, height=150, relief=SUNKEN, borderwidth=2)
IncScrollFrame = ScrollFrame(IncListCont, height=150)
netInc = Label(IncListCont,text='Net Income: ',font=("Calibri", 14))
addInc = Button(IncFrame,text='Add Income',font=("Calibri", 14),command=addIncome)
chartI = Button(IncFrame,text='Generate Graph',font=("Calibri", 14))
LabelIn1.grid(row=0,column=0,sticky=N)
CanvChartInc.grid(row=1,column=0,columnspan=2,padx=10,pady=10,sticky=NSEW)
IncListCont.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=NSEW)
IncListCont.grid_propagate(False)
IncScrollFrame.pack(fill="both", expand=True)
netInc.pack(fill="both", expand=True)
addInc.grid(row=4,column=0,padx=5,pady=5,sticky=NSEW)
chartI.grid(row=4,column=1,padx=5,pady=5,sticky=NSEW)

#NextPrev-Button Frame
NextTP = Button(NextPrev,text='  Next Timespan  ',font=("Calibri", 12))
PrevTp = Button(NextPrev,text='Previous Timespan',font=("Calibri", 12))
NextTP.pack(side=LEFT)
PrevTp.pack(side=LEFT)

#LineGraph Frame Widgets
LabelLin1 = Label(LineFrame,text='Expense vs Income over a period of time:',font=("Calibri", 14))
CanvChartLine = Canvas(LineFrame,bg='pink')
chartL = Button(LineFrame,text='Generate Graph',font=("Calibri", 14))
grossTotal = Frame(LineFrame,bg="yellow",width=200,height=100,relief=SUNKEN,borderwidth=2)
expTotal = Frame(LineFrame,bg="yellow",width=200,height=100,relief=SUNKEN,borderwidth=2)
netTotal = Frame(LineFrame,bg="yellow",width=200,height=100,relief=SUNKEN,borderwidth=2)
LabelLin1.grid(row=0,column=0,columnspan=2,sticky=N)
CanvChartLine.grid(row=1,column=0,columnspan=2,padx=10,pady=10,sticky=NSEW)
chartL.grid(row=2,column=0,columnspan=2,sticky=N)
grossTotal.grid(row=3,column=0,columnspan=2,sticky=N)
expTotal.grid(row=4,column=0,columnspan=2,sticky=N)
netTotal.grid(row=5,column=0,columnspan=2,sticky=N)




root.mainloop()