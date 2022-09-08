import tkinter as tk
from tkinter import ttk
from tkinter import *
import sqlite3
import pickle
from tkinter.constants import END
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
class showPlan(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pageTitle=tk.Label(self, text='Plan', font=("Times New Roman", 25))
        pageTitle.place(x=450, y=0)

        labelVar = StringVar()
        labelVar2 = StringVar()
        labelVar3 = StringVar()

        moneyLeftSpending = tk.Label(self, textvariable=labelVar, borderwidth=2, relief="solid")

        moneyInSavings = tk.Label(self, textvariable=labelVar2, borderwidth=2, relief="solid")

        percentLeft = tk.Label(self, textvariable=labelVar3, borderwidth=2, relief="solid")

        def updatePlan():

            con1 = sqlite3.connect('plan.db')
            cur1 = con1.cursor()

            cur1.execute('SELECT * FROM table1')
            data = cur1.fetchall()


            for x in data:

                con1 = sqlite3.connect('incomes.db')
                cur1 = con1.cursor()

                cur1.execute('SELECT SUM(moneySpending) FROM table1')
                allSpending = cur1.fetchone()[0]

                con1.close()

                con1 = sqlite3.connect('plan.db')
                cur1 = con1.cursor()

                updateMoney = """Update table1 set moneyBudgeted = ? where category = ?"""
                moneyData = (round(float(x[2])*float(allSpending), 2), x[0],)

                cur1.execute(updateMoney, moneyData)

                con1.commit()
                con1.close()

            viewPlan()

            updateLabels()

        def updateLabels():
            tk.Label(self, text='$ to Spend').place(x=150,y=140)
            tk.Label(self, text='Savings').place(x=350, y=140)
            tk.Label(self, text='% ' + 'Left to Budget').place(x=500, y=140)

            con1 = sqlite3.connect('plan.db')
            cur1 = con1.cursor()

            cur1.execute('SELECT SUM(moneyBudgeted) FROM table1')
            totalBudgeted = cur1.fetchone()[0]

            con1.close()


            con1 = sqlite3.connect('incomes.db')
            cur1 = con1.cursor()

            cur1.execute('SELECT SUM(moneySavings) FROM table1')
            allSavings = cur1.fetchone()[0]

            con1.close()

            con1 = sqlite3.connect('incomes.db')
            cur1 = con1.cursor()

            cur1.execute('SELECT SUM(moneySpending) FROM table1')
            allSpending = cur1.fetchone()[0]

            con1.close()

            con1 = sqlite3.connect('plan.db')
            cur1 = con1.cursor()

            cur1.execute('SELECT SUM(percentageOfIncome) FROM table1')
            totalPercent = cur1.fetchone()[0]

            con1.close()


            labelVar.set(round(float(allSpending)-float(totalBudgeted), 2))
            moneyLeftSpending.place(x=150,y=170)

            labelVar2.set(float(allSavings))
            moneyInSavings.place(x=350,y=170)

            labelVar3.set(round(float(1-totalPercent), 2))
            percentLeft.place(x=500, y=170)



        def inputCategories():

            OPTIONS = []
            with open('categories', 'rb') as f:    
                categoryList = pickle.load(f)
                OPTIONS.extend(categoryList)

            

            for x in OPTIONS[1:]:

                con1 = sqlite3.connect('plan.db')
                cur1 = con1.cursor()

                cur1.execute("SELECT category FROM table1")
                categories1=cur1.fetchall()
                categories1=[i[0] for i in categories1]
                if x not in categories1:
        
                    con1 = sqlite3.connect(x + '.db')
                    cur1 = con1.cursor()

                    cur1.execute('SELECT SUM(moneySpent) FROM table1')
                    defaultBudget = cur1.fetchone()[0]

                    con1.close()

                    con1 = sqlite3.connect('incomes.db')
                    cur1 = con1.cursor()

                    cur1.execute('SELECT SUM(moneySpending) FROM table1')
                    allSpending = cur1.fetchone()[0]

                    con1.close()

                    con1 = sqlite3.connect('plan.db')
                    cur1 = con1.cursor()
                    cur1.execute('''
                    INSERT INTO table1 (category, moneyBudgeted, percentageOfIncome)

                        VALUES
                        (?, ?, ?)
                    ''',(x, float(defaultBudget), round(float(defaultBudget)/float(allSpending), 4)))
        
                    con1.commit()

                    con1.close()

                con1.close() 

                updateLabels()

                viewPlan()


        def viewPlan():


            tree = ttk.Treeview(self, height = 15, column=("c1", "c2", "c3"), show='headings')

            tree.column("#1", anchor=tk.CENTER)

            tree.heading("#1", text="Category")

            tree.column("#2", anchor=tk.CENTER)

            tree.heading("#2", text="$ Budgeted")

            tree.column("#3", anchor=tk.CENTER)

            tree.heading("#3", text="Percent of Spending Income")

            tree.place(x=150,y=200)


            con1 = sqlite3.connect('plan.db')

            cur1 = con1.cursor()

            cur1.execute("SELECT * FROM table1")

            rows = cur1.fetchall() 

            for row in rows:

                print(row) 

                tree.insert("", tk.END, values=row)

            con1.close()

        def changePercentage():


            def changeSQL():

                con1 = sqlite3.connect('incomes.db')
                cur1 = con1.cursor()

                cur1.execute('SELECT SUM(moneySpending) FROM table1')
                allSpending = cur1.fetchone()[0]

                con1.close()

                con1 = sqlite3.connect('plan.db')

                cur1 = con1.cursor()

                updatePercentage = """Update table1 set percentageOfIncome = ? where category = ?"""
                updateMoney = """Update table1 set moneyBudgeted = ? where category = ?"""
                percentData = (float(percentageInput.get()), variable2.get())
                moneyData = (float(percentageInput.get())*float(allSpending), variable2.get())

                cur1.execute(updatePercentage, percentData)
                cur1.execute(updateMoney, moneyData)

                con1.commit()
                con1.close()

                updateLabels()

                viewPlan()

                percentageInput.destroy()
                percentageLabel.destroy()
                submitPerentage.destroy()
                categorySelect.destroy()

            OPTIONS = []
            with open('categories', 'rb') as f:    
                categoryList = pickle.load(f)
                OPTIONS.extend(categoryList)

            variable2 = StringVar(self)
            variable2.set(OPTIONS[0]) # default value
    
            categorySelect = OptionMenu(self, variable2, *OPTIONS)
            categorySelect.grid(row=2)

            percentageInput = tk.Entry(self)
            percentageLabel=tk.Label(self, text="Enter Percentage (Decimal Form):")
            percentageLabel.grid(row=3, column=0)
            percentageInput.grid(row=3,column=1)
            submitPerentage = tk.Button(self, text="Submit", command=changeSQL)
            submitPerentage.grid(row=4, column=1)

            


        showPlanButton=tk.Button(self, text="Show Plan", command=inputCategories)
        showPlanButton.grid(row=0, column=0)

        changePercentButton = tk.Button(self, text="Change Percentage", command=changePercentage)
        changePercentButton.grid(row=1, column=0)

        updatePlanButton = tk.Button(self, text="Update Plan", command=updatePlan)
        updatePlanButton.grid(row=0, column=1)
 


        
    
        


