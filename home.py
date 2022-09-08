import tkinter as tk
from tkinter.constants import CENTER
from income import showIncome
from expenses import showExpenses
from goals import showGoals
from plan import showPlan
from tkinter.ttk import Label
import sqlite3
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class showHome(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pageTitle=Label(self, text='Home Page', font=("Times New Roman", 25))
        pageTitle.place(x=450, y=0)
        instructions=tk.Label(self, text='Welcome to my Budget Planner. To get started, head on over to the Income tab and enter the Date and Amount Recieved (no need for the $ sign). \nOnce you have entered some incomes, you will be ready to enter your expenses. Navigate to the Expenses tab and Create a New Category in which your expense falls in. \nOnce you have created your category, enter in the Date, Transaction Name, and $ Spent. Click Submit and you are set. \nIf you wish to repeat the steps and add more expenses, make sure to select the category you wish to enter in first before you input the information. \nYou can also create more Categories. Once you have entered your expenses in, you are ready to plan and budget your money. \nHead to the Plan tab. You will see each of your categories and the $ Budgeted for it. This value defaults to the $ Spent in that Category when you first view the Plan or make a Category. \nIf you would like to change the $ Budgeted, click the Change Percantage Button and select the Category you wish to change and enter the new Percentage. \nThis new percentage budgets the category from your Total $ to Spend. \nAt the top, there are provided labels that help you track how much $ is left to Spend and how much % is left of your Total Spending while you budget your categories. \nIf you decide to go back and add more incomes or categories, make sure to click the Update Plan Button when you revisit the Plan Page. \nFinally, we have the Goals Page. Create a New Goal you want to reach for either your Total Savings or Total $ to Spend. \nCome back any time and see your progress on the goals by clicking the buttons on the top right of the Goals Page.', font=("Times New Roman", 15))
        instructions.place(x=50,y=100)
        con1 = sqlite3.connect('incomes.db')

        cur1 = con1.cursor()

        cur1.execute("CREATE TABLE IF NOT EXISTS table1(date TEXT, moneyRecieved TEXT, moneySpending TEXT, moneySavings TEXT)")

        con1.commit()
        con1.close()

        con1 = sqlite3.connect('plan.db')

        cur1 = con1.cursor()

        cur1.execute("CREATE TABLE IF NOT EXISTS table1(category TEXT, moneyBudgeted FLOAT, percentageOfIncome TEXT)")

        con1.commit()
        con1.close()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        pageHome = showHome(self)
        pageIncome = showIncome(self)
        pageExpenses = showExpenses(self)
        pagePlan = showPlan(self)
        pageGoals = showGoals(self)

        buttons = tk.Frame(self)
        buttonsBar = tk.Frame(self)
        buttons.pack(side="top", fill="x", expand=False)
        buttonsBar.pack(side="top", fill="both", expand=True)

        pageHome.place(in_=buttonsBar, x=0, y=0, relwidth=1, relheight=1)
        pageIncome.place(in_=buttonsBar, x=0, y=0, relwidth=1, relheight=1)
        pageExpenses.place(in_=buttonsBar, x=0, y=0, relwidth=1, relheight=1)
        pagePlan.place(in_=buttonsBar, x=0, y=0, relwidth=1, relheight=1)
        pageGoals.place(in_=buttonsBar, x=0, y=0, relwidth=1, relheight=1)


        b1 = tk.Button(buttons, text="Home", command=pageHome.show)
        b2 = tk.Button(buttons, text="Income", command=pageIncome.show)
        b3 = tk.Button(buttons, text="Expenses", command=pageExpenses.show)
        b4 = tk.Button(buttons, text="Plan", command=pagePlan.show)
        b5 = tk.Button(buttons, text="Goals", command=pageGoals.show)


        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")

        pageHome.show()

if __name__ == "__main__":
    home = tk.Tk()
    main = MainView(home)
    main.pack(side="top", fill="both", expand=True)
    home.wm_geometry("1920x1080")
    home.title('Budget Planner')
    home.mainloop()



