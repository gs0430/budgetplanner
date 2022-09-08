import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter.constants import END
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class showIncome(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pageTitle=tk.Label(self, text='Income', font=("Times New Roman", 25))
        pageTitle.place(x=600, y=0)
        tk.Label(self, text="Enter Date").grid(row=0)
        tk.Label(self, text="Enter $ Receieved").grid(row=1)
        e1 = tk.Entry(self)
        e2 = tk.Entry(self)
        e1.grid(row=0, column=1)
        e2.grid(row=1, column=1)
        
        def View():
            
            tk.Label(self, text="Total $ Received").place(x=400, y=40)
            tk.Label(self, text="Total $ to Spend").place(x=600, y=40)
            tk.Label(self, text="Total $ to Save").place(x=800, y=40)

            tree = ttk.Treeview(self, height = 35, column=("c1", "c2", "c3", "c4"), show='headings')

            tree.column("#1", anchor=tk.CENTER)

            tree.heading("#1", text="Date")

            tree.column("#2", anchor=tk.CENTER)

            tree.heading("#2", text="$ Recieved")

            tree.column("#3", anchor=tk.CENTER)

            tree.heading("#3", text="$ to Spend")

            tree.column("#4", anchor=tk.CENTER)

            tree.heading("#4", text="$ to Savings")

            tree.place(x=150,y=100)


            con1 = sqlite3.connect('incomes.db')

            cur1 = con1.cursor()

            cur1.execute("SELECT * FROM table1")

            rows = cur1.fetchall() 

            for row in rows:

                print(row) 

                tree.insert("", tk.END, values=row)

            cur1.execute('SELECT SUM(moneyRecieved) FROM table1')
            totalRecieved = cur1.fetchone()[0]

            cur1.execute('SELECT SUM(moneySpending) FROM table1')
            totalSpending = cur1.fetchone()[0]

            cur1.execute('SELECT SUM(moneySavings) FROM table1')
            totalSavings = cur1.fetchone()[0]

            con1.close() 

            tk.Label(self,text=totalRecieved, borderwidth=2, relief="solid").place(x=425, y=70)
            tk.Label(self,text=totalSpending, borderwidth=2, relief="solid").place(x=625, y=70)
            tk.Label(self,text=totalSavings, borderwidth=2, relief="solid").place(x=825, y=70)


        
        def inputValues():

            con1 = sqlite3.connect('incomes.db')
            cur1 = con1.cursor()
            cur1.execute('''
            INSERT INTO table1 (date, moneyRecieved, moneySpending, moneySavings)

                VALUES
                (?, ?, ?, ?)
            ''',(e1.get(), float(e2.get()), round(float(e2.get())*(0.70), 2), float(e2.get())-round(float(e2.get())*(0.70), 2)))
        
            con1.commit()

            con1.close()

            e1.delete(0,END)
            e2.delete(0,END)
            
            View()
        submitButton = tk.Button(self, text='Submit', command=inputValues)
        submitButton.place(x=10,y=60)

        showIncomeTable=tk.Button(self, text="Show Incomes", command=View)
        showIncomeTable.place(x=100, y=60)
