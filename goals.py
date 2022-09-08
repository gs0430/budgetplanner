import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
import pickle
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()
class showGoals(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        pageTitle=tk.Label(self, text='Goals', font=("Times New Roman", 25))
        pageTitle.place(x=450, y=0)
        def spendingGoal():

            def submitSpendingGoal():
                spendingGoalValue=float(spendingEntry.get())
                with open('spendingGoal', 'wb') as f:
                    pickle.dump(spendingGoalValue, f)

                con1 = sqlite3.connect('incomes.db')

                cur1 = con1.cursor()
                cur1.execute('SELECT SUM(moneySpending) FROM table1')
                totalSpending = cur1.fetchone()[0]

                con1.close()


                spendingGoalY = ['Total $ Spending']
                moneyX = [float(totalSpending)]
                
                plt.figure(figsize=(10,5))
                plt.barh(spendingGoalY,moneyX, height=1)
                plt.xlim([0,spendingGoalValue])
                plt.title('Spending Goal')
                plt.xlabel('$')
                for index, value in enumerate(moneyX):
                    plt.text(value + 2, index, str(value), va='center')
                plt.show()

                spendingLabel.destroy()
                spendingEntry.destroy()
                submitSpendingButton.destroy()


            spendingLabel=tk.Label(self, text='Enter Spending $ Goal')
            spendingLabel.grid(row=2)
            spendingEntry=tk.Entry(self)
            spendingEntry.grid(row=3)
            submitSpendingButton=tk.Button(self, text="Submit", command=submitSpendingGoal)
            submitSpendingButton.grid(row=4)


        def savingsGoal():
            def submitSavingsGoal():
                savingsGoalValue=float(savingsEntry.get())
                with open('savingsGoal', 'wb') as f:
                    pickle.dump(savingsGoalValue, f)

                con1 = sqlite3.connect('incomes.db')

                cur1 = con1.cursor()
                cur1.execute('SELECT SUM(moneySavings) FROM table1')
                totalSavings = cur1.fetchone()[0]

                con1.close()


                savingsGoalY = ['Total $ Savings']
                savingsMoneyX = [float(totalSavings)]
                
                plt.figure(figsize=(10,5))
                plt.barh(savingsGoalY,savingsMoneyX, height=1)
                plt.xlim([0,savingsGoalValue])
                plt.title('Savings Goal')
                plt.xlabel('$')

                for index, value in enumerate(savingsMoneyX):
                    plt.text(value + 2, index, str(value), va='center')
                plt.show()

                savingsLabel.destroy()
                savingsEntry.destroy()
                submitSavingsButton.destroy()

            savingsLabel=tk.Label(self, text='Enter Savings $ Goal')
            savingsLabel.grid(row=2,column=1)
            savingsEntry=tk.Entry(self)
            savingsEntry.grid(row=3,column=1)
            submitSavingsButton=tk.Button(self, text="Submit", command=submitSavingsGoal)
            submitSavingsButton.grid(row=4,column=1)

        def newGoal():
            spendingButton=tk.Button(self, text="Spending Goal", command=spendingGoal)
            spendingButton.grid(row=1)

            savingsButton=tk.Button(self, text="Savings Goal", command=savingsGoal)
            savingsButton.grid(row=1, column=1)

        def showSpendingGoal():
            with open('spendingGoal', 'rb') as f:    
                spendingGoalValue = pickle.load(f)

            con1 = sqlite3.connect('incomes.db')

            cur1 = con1.cursor()
            cur1.execute('SELECT SUM(moneySpending) FROM table1')
            totalSpending = cur1.fetchone()[0]

            con1.close()


            spendingGoalY = ['Total $ Spending']
            moneyX = [float(totalSpending)]
            plt.figure(figsize=(10,5))
            plt.barh(spendingGoalY,moneyX, height=1)
            plt.xlim([0,spendingGoalValue])
            plt.title('Spending Goal')
            plt.xlabel('$')
            for index, value in enumerate(moneyX):
                plt.text(value + 2, index, str(value), va='center')
            plt.show()

        def showSavingsGoal():
            with open('savingsGoal', 'rb') as f:    
                savingsGoalValue = pickle.load(f)

            con1 = sqlite3.connect('incomes.db')

            cur1 = con1.cursor()
            cur1.execute('SELECT SUM(moneySavings) FROM table1')
            totalSavings = cur1.fetchone()[0]

            con1.close()


            savingsGoalY = ['Total $ Savings']
            savingsMoneyX = [float(totalSavings)]
            plt.figure(figsize=(10,5))
            plt.barh(savingsGoalY,savingsMoneyX, height=1)
            plt.xlim([0,savingsGoalValue])
            plt.title('Savings Goal')
            plt.xlabel('$')
            for index, value in enumerate(savingsMoneyX):
                plt.text(value + 2, index, str(value), va='center')
            plt.show()



        tk.Button(self, text='Make New Goal', command=newGoal).grid(row=0)
        tk.Button(self, text='Show Current\nSpending Goal', command=showSpendingGoal).place(x=1100, y=0)
        tk.Button(self, text='Show Current\nSavings Goal', command=showSavingsGoal).place(x=1250, y=0)