import tkinter as tk
from tkinter import *
from tkinter import ttk
import pickle
import sqlite3
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
class showExpenses(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pageTitle=tk.Label(self, text='Expenses', font=("Times New Roman", 25))
        pageTitle.place(x=600, y=0)

        OPTIONS = []
        try:
            with open('categories', 'rb') as f:    
                categoryList = pickle.load(f)
                OPTIONS.extend(categoryList)

                
        except:
            OPTIONS = [
            "Select Category"
            ]

        variable = StringVar(self)
        variable.set(OPTIONS[0]) # default value
    
        categorySelect = OptionMenu(self, variable, *OPTIONS)
        categorySelect.grid(row=0)
        tk.Label(self, text="Enter Date").grid(row=3)
        tk.Label(self, text="Enter Transcation Name").grid(row=4)
        tk.Label(self, text="Enter $ Spent").grid(row=5)

        g1 = tk.Entry(self)
        g2 = tk.Entry(self)
        g3 = tk.Entry(self)
        g1.grid(row=3, column=1)
        g2.grid(row=4, column=1)
        g3.grid(row=5, column=1)

        labelVar = StringVar()
        labelVar2 = StringVar()
        expenseCategory = tk.Label(self,textvariable=labelVar, borderwidth=2, relief="solid")
        totalExpenseLabel = tk.Label(self,textvariable=labelVar2, borderwidth=2, relief="solid")

            

        labelVar3 = StringVar()
        categoryBudget = tk.Label(self,textvariable=labelVar3,  borderwidth=2, relief="solid")

        def viewSQL():
            tk.Label(self, text="Category").place(x=400, y=40)
            tk.Label(self, text="Total $ Spent").place(x=600, y=40)
            tk.Label(self, text="Category Budget").place(x=800, y=40)


            tree = ttk.Treeview(self, height = 35, column=("c1", "c2", "c3", "c4"), show='headings')
            tree.column("#1", anchor=tk.CENTER)

            tree.heading("#1", text="Date")

            tree.column("#2", anchor=tk.CENTER)

            tree.heading("#2", text="Name")

            tree.column("#3", anchor=tk.CENTER)

            tree.heading("#3", text="$ Spent")

            tree.column("#4", anchor=tk.CENTER)

            tree.heading("#4", text="Category")

            tree.place(x=400,y=100)


            con1 = sqlite3.connect(variable.get()+'.db')

            cur1 = con1.cursor()

            cur1.execute("SELECT * FROM table1")

            rows = cur1.fetchall() 

            for row in rows:

                print(row) 

                tree.insert("", tk.END, values=row)

            cur1.execute('SELECT SUM(moneySpent) FROM table1')
            totalSpent = cur1.fetchone()[0]

            con1.close()

            labelVar.set(variable.get())
            expenseCategory.place(x=400, y=70)

            labelVar2.set(totalSpent)
            totalExpenseLabel.place(x=625, y=70)


            con1 = sqlite3.connect('plan.db')

            cur1 = con1.cursor()

            cur1.execute('SELECT * FROM table1')
            data = cur1.fetchall()


            for x in data:
                if x[0] == variable.get():
                    labelVar3.set(x[1])
                    categoryBudget.place(x=800, y=70)



            con1.close()


        def createCategory():
            categoryInput = tk.Entry(self)
            newCategoryLabel=tk.Label(self, text="Enter Category Name:")
            newCategoryLabel.grid(row=0, column=1)
            categoryInput.grid(row=1,column=1)

            def submitCategory():
                OPTIONS.append(categoryInput.get())
                OptionMenu(self, variable, *OPTIONS).grid(row=0)
                with open('categories', 'wb') as f:
                    pickle.dump(OPTIONS, f)

                con1 = sqlite3.connect(categoryInput.get()+'.db')

                cur1 = con1.cursor()

                cur1.execute("CREATE TABLE IF NOT EXISTS table1(date TEXT,  Name TEXT, moneySpent TEXT, Category TEXT)")

                con1.commit()
                con1.close()



                variable.set(categoryInput.get())
                newCategoryLabel.destroy()
                submitButton.destroy()
                categoryInput.destroy()
        
            submitButton=tk.Button(self, text="Submit", command = submitCategory)
            submitButton.grid(row=0,column=3)

        def inputExpenses():
            con1 = sqlite3.connect(variable.get()+'.db')
            cur1 = con1.cursor()
            cur1.execute('''
            INSERT INTO table1 (date, Name, moneySpent, Category)

                VALUES
                (?, ?, ?, ?)
            ''',(g1.get(), g2.get(), float(g3.get()), variable.get()))
        
            con1.commit()

            con1.close()

            g1.delete(0,END)
            g2.delete(0,END)
            g3.delete(0,END)

            
            viewSQL()
            

        tk.Button(self, text="New Category", command=createCategory).grid(row=1)
        tk.Button(self, text="Submit", command = inputExpenses).grid(row=6)

        showExpenseTable=tk.Button(self, text="Show Expenses", command=viewSQL)
        showExpenseTable.grid(row=7)

        




