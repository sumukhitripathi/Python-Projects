import csv
import os
def expense_input(): #User input for daily expenses
    fields=['Month','Category','Amount']
    rows=[]
    print('The categories are:\n 1. Food\n 2. Entertainment\n 3. Transport\n 4. Misc')
    while True:
        month=input("Enter the month: ")
        category=input("Enter the category: ")
        amount=input("Enter the amount: ")
        if not amount.isdigit():
            print("Amount should be a number")
            continue
        rows.append([month,category,amount])
        choice=input("Do you want to add more records? (y/n): ")
        if choice=='n' or choice=='N':
            break
    file_exists = os.path.exists('expenses.csv')

    with open('expenses.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(fields)  # write into the file
        writer.writerows(rows)

def expense_summary(n):  #spending pattern...monthly summary & category wise expenditure
    if not os.path.exists('expenses.csv'):
        print("No expense records found!")
        return
    with open('expenses.csv', 'r') as f:   #read from file
        reader = list(csv.reader(f))       #store as list
    
    if (n == 1):
        mon = input("Which month's summary to check? ").strip()
        records = [row for row in reader[1:] if row[0].lower() == mon.lower()]
        
        if records:
            total = sum([float(row[2]) for row in records])
            print("\nExpenses for", mon)
            for row in records:
                print('Category: ',row[1],'\tAmount: ',row[2])
            print('Total for ',mon,': ',total)
        else:
            print("No expenses found for this month.")

    elif n == 2:
        catg = input("Which category summary to check? ").strip()
        records = [row for row in reader[1:] if row[1].lower() == catg.lower()]
        
        if records:
            total = sum([float(row[2]) for row in records])
            print("\nExpenses under", catg)
            for row in records:
                print('Month: ',row[0],'\tAmount: ',row[2])
            print('Total for ',catg,': ',total)
        else:
            print("No expenses found for this category.")

    else:
        print("Invalid choice! Please enter 1 or 2.")

def main():
    choice=input("Do you want to add expense records? (y/n): ")
    if (choice=='y' or choice=='Y'):
        expense_input()
    elif choice not in ('y','Y','n','N'):
        print("Wrong choice")
    while True:
        try:
            n=int(input('Do you want to check the monthly summary or category wise expenditure or exit? (1/2/3): '))
            if (n==1 or n==2):
                expense_summary(n)
            elif (n==3):
                break
        except ValueError:
                print("Wrong choice")
            
main()