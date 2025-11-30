# I'll insert a cleaned + fixed version of your file with the graph containment fix
# and the clear/reload logic properly implemented.

# Due to length, this document will contain the FULL corrected code.
# --- CODE FOLLOWS ---

from tkinter import *
from tkinter.ttk import Combobox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkcalendar import DateEntry
from datetime import *
import numpy as np

root = Tk()
root.geometry("1080x720")
root.minsize(1080,720)
root.title("Income Management System")

# global storages
expense_data = []
income_data = []
totals_by_span = {"Weeks": [], "Months": [], "Years": []}
varTimeSpan = StringVar(value="Weeks")

# --- amount validators

def validate_amount(text):
    if text == "": return True
    return text.replace(".", "", 1).isdigit()

vcmd = (root.register(validate_amount), "%P")

# --- scroll frame
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
        self._window_id = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        def _update_scroll(e):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.scrollable_frame.bind("<Configure>", _update_scroll)

        def _canvas_width(e):
            self.canvas.itemconfig(self._window_id, width=e.width)
        self.canvas.bind("<Configure>", _canvas_width)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vscroll.pack(side="right", fill="y")


# --- Base chart class with proper clearing
class BaseChart:
    def __init__(self, frame):
        self.frame = frame
        self.canvas_widget = None
        self.toolbar = None

    def clear(self):
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()
            self.canvas_widget = None
        if self.toolbar:
            self.toolbar.destroy()
            self.toolbar = None

    def embed(self, fig):
        self.clear()
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self.frame)
        toolbar.update()
        self.canvas_widget = canvas
        self.toolbar = toolbar


# --- Pie chart
class PieChart(BaseChart):
    def __init__(self, frame):
        super().__init__(frame)

    def render(self, expense_data, total_label):
        labels = []
        amounts = []
        total = 0

        for rec in expense_data:
            cat = rec["category"].get().strip()
            v = rec["amount"].get().strip()
            if cat != '' and v.replace('.', '', 1).isdigit():
                val = float(v)
                labels.append(cat)
                amounts.append(val)
                total += val

        total_label.config(text=f"Total Expenses: {total:.2f}")

        fig = Figure(figsize=(3,3), dpi=100)
        ax = fig.add_subplot(111)
        if amounts:
            ax.pie(amounts, labels=labels, autopct='%1.1f%%')
        else:
            ax.text(0.5,0.5,'No data',ha='center')

        self.embed(fig)


# --- Bar Chart
class BarChart(BaseChart):
    def __init__(self, frame):
        super().__init__(frame)

    def render(self, income_data, expense_data, net_label):
        labels = []
        amounts = []
        income_total = 0
        for rec in income_data:
            cat = rec["category"].get().strip()
            v = rec["amount"].get().strip()
            if cat != '' and v.replace('.', '', 1).isdigit():
                val = float(v)
                labels.append(cat)
                amounts.append(val)
                income_total += val

        expense_total = sum(float(r["amount"].get()) for r in expense_data if r["amount"].get().replace('.', '', 1).isdigit())
        net_label.config(text=f"Net Income: {income_total - expense_total:.2f}")

        fig = Figure(figsize=(3,3), dpi=100)
        ax = fig.add_subplot(111)

        if amounts:
            x = np.arange(len(amounts))
            ax.bar(x, amounts)
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha="right")
        else:
            ax.text(0.5,0.5,'No data',ha='center')

        self.embed(fig)


# --- Line Chart
class LineChart(BaseChart):
    def __init__(self, frame):
        super().__init__(frame)

    def render(self, totals_by_span, span):
        data = totals_by_span.get(span, [])
        fig = Figure(figsize=(3,3), dpi=100)
        ax = fig.add_subplot(111)

        if not data:
            ax.text(0.5, 0.5, f'No data for {span}', ha='center')
        else:
            x = [f"{span[:-1]} {i+1}" for i in range(len(data))]
            inc = [d['income'] for d in data]
            exp = [d['expense'] for d in data]
            net = [d['net'] for d in data]

            ax.plot(x, inc, marker='o', label='Income')
            ax.plot(x, exp, marker='o', label='Expense')
            ax.plot(x, net, marker='o', label='Net')
            ax.legend()

        self.embed(fig)


# GUI containers
main = Frame(root)
main.pack(fill="both", expand=True)
main.grid_columnconfigure((0,1,2), weight=1)

# Expense frame
expF = Frame(main, bg='white')
expF.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
chartExpFrame = Frame(expF, bg='lightgrey')
chartExpFrame.grid(row=1, column=0, columnspan=2, sticky='nsew')
pie_chart = PieChart(chartExpFrame)
ExpListCont = Frame(expF, bg="lightgrey")
ExpListCont.grid(row=3, column=0, columnspan=2, sticky='nsew')
ExpScroll = ScrollFrame(ExpListCont, height=150)
ExpScroll.pack(fill='both', expand=True)
totExp = Label(ExpListCont, text="Total Expenses: 0")
totExp.pack(fill='both')

# Income frame
incF = Frame(main, bg='white')
incF.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
chartIncFrame = Frame(incF, bg='lightgrey')
chartIncFrame.grid(row=1, column=0, columnspan=2, sticky='nsew')
bar_chart = BarChart(chartIncFrame)
IncListCont = Frame(incF, bg='lightgrey')
IncListCont.grid(row=3, column=0, columnspan=2, sticky='nsew')
IncScroll = ScrollFrame(IncListCont, height=150)
IncScroll.pack(fill='both', expand=True)
netInc = Label(IncListCont, text="Net Income: 0")
netInc.pack(fill='both')

# Line frame
lineF = Frame(main, bg='white')
lineF.grid(row=0, column=2, sticky='nsew', padx=5, pady=5)
chartLineFrame = Frame(lineF, bg='lightgrey')
chartLineFrame.grid(row=1, column=0, sticky='nsew')
line_chart = LineChart(chartLineFrame)

def addExpense():
    row = len(expense_data)
    parent = ExpScroll.scrollable_frame
    e1 = Entry(parent)
    e2 = Entry(parent, validate='key', validatecommand=vcmd)
    e1.grid(row=row, column=0, sticky='nsew')
    e2.grid(row=row, column=1, sticky='nsew')
    expense_data.append({"category": e1, "amount": e2})

def addIncome():
    row = len(income_data)
    parent = IncScroll.scrollable_frame
    e1 = Entry(parent)
    e2 = Entry(parent, validate='key', validatecommand=vcmd)
    e1.grid(row=row, column=0, sticky='nsew')
    e2.grid(row=row, column=1, sticky='nsew')
    income_data.append({"category": e1, "amount": e2})

BtnExpAdd = Button(expF, text="Add Expense", command=addExpense)
BtnExpAdd.grid(row=4, column=0, sticky='nsew')
BtnExpGen = Button(expF, text="Generate Chart", command=lambda: pie_chart.render(expense_data, totExp))
BtnExpGen.grid(row=4, column=1, sticky='nsew')

BtnIncAdd = Button(incF, text="Add Income", command=addIncome)
BtnIncAdd.grid(row=4, column=0, sticky='nsew')
BtnIncGen = Button(incF, text="Generate Graph", command=lambda: bar_chart.render(income_data, expense_data, netInc))
BtnIncGen.grid(row=4, column=1, sticky='nsew')

# Date + span controls
dateSpanFrame = Frame(expF)
dateSpanFrame.grid(row=2, column=0, columnspan=2)
DateSel = DateEntry(dateSpanFrame)
DateSel.pack(side='left')
spanSel = Combobox(dateSpanFrame, values=['Weeks','Months','Years'], textvariable=varTimeSpan, state='readonly')
spanSel.pack(side='left')

# generate results
BtnLineGen = Button(lineF, text='Generate Results', command=lambda: generate_results())
BtnLineGen.grid(row=2, column=0, sticky='nsew')

def generate_results():
    span = varTimeSpan.get()
    d = DateSel.get()
    inc = sum(float(r['amount'].get()) for r in income_data if r['amount'].get().replace('.', '', 1).isdigit())
    exp = sum(float(r['amount'].get()) for r in expense_data if r['amount'].get().replace('.', '', 1).isdigit())
    net = inc-exp
    existing = next((x for x in totals_by_span[span] if x['start_date']==d), None)
    if existing:
        existing.update({'income':inc,'expense':exp,'net':net})
    else:
        totals_by_span[span].append({'start_date':d,'income':inc,'expense':exp,'net':net})
    line_chart.render(totals_by_span, span)

root.mainloop()
