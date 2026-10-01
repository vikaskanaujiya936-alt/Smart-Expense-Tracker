import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


def add_expense():
    name = input("Enter expense name: ")
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")

    date = datetime.now().strftime("%d-%m-%Y")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, name, category, amount])

    print("Expense saved successfully!")


def view_expenses():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = list(csv.reader(file))

        if not expenses:
            print("No expenses found.")
            return

        print("\n===== ALL EXPENSES =====")
        total = 0

        for i, row in enumerate(expenses, start=1):
            if len(row) == 4:
                date, name, category, amount = row
                print(i, "|", date, "|", name, "|", category, "| ₹", amount)
                total += float(amount)

        print("-------------------------")
        print("Total Expense: ₹", total)

    except FileNotFoundError:
        print("No expenses found.")


def delete_expense():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = list(csv.reader(file))

        if not expenses:
            print("No expenses found.")
            return

        for i, row in enumerate(expenses, start=1):
            print(i, "|", row[0], "|", row[1], "|", row[2], "| ₹", row[3])

        number = int(input("Enter expense number to delete: "))

        if number < 1 or number > len(expenses):
            print("Invalid expense number.")
            return

        deleted = expenses.pop(number - 1)

        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(expenses)

        print("Deleted:", deleted[1])
        print("Expense deleted successfully!")

    except FileNotFoundError:
        print("No expenses found.")
    except ValueError:
        print("Please enter a valid number.")


def category_summary():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = list(csv.reader(file))

        summary = {}

        for row in expenses:
            if len(row) == 4:
                category = row[2]
                amount = float(row[3])
                summary[category] = summary.get(category, 0) + amount

        print("\n===== CATEGORY SUMMARY =====")

        for category, amount in summary.items():
            print(category, ": ₹", amount)

    except FileNotFoundError:
        print("No expenses found.")


def monthly_summary():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = list(csv.reader(file))

        month = input("Enter month (MM-YYYY): ")
        total = 0

        for row in expenses:
            if len(row) == 4:
                if row[0][3:] == month:
                    total += float(row[3])

        print("\n===== MONTHLY SUMMARY =====")
        print("Month:", month)
        print("Total Expense: ₹", total)

    except FileNotFoundError:
        print("No expenses found.")


def search_expense():
    try:
        with open(FILE_NAME, "r") as file:
            expenses = list(csv.reader(file))

        if not expenses:
            print("No expenses found.")
            return

        keyword = input("Search by name or category: ").lower()

        found = False

        print("\n===== SEARCH RESULTS =====")

        for row in expenses:
            if len(row) == 4:
                date, name, category, amount = row

                if keyword in name.lower() or keyword in category.lower():
                    print(
                        date, "|",
                        name, "|",
                        category, "| ₹", amount
                    )
                    found = True

        if not found:
            print("No matching expense found.")

    except FileNotFoundError:
        print("No expenses found.")


while True:

    print("\n===== SMART EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Delete Expense")
    print("4. Category Summary")
    print("5. Monthly Summary")
    print("6. Search Expense")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        delete_expense()

    elif choice == "4":
        category_summary()

    elif choice == "5":
        monthly_summary()

    elif choice == "6":
        search_expense()

    elif choice == "7":
        print("Thank you for using Smart Expense Tracker!")
        break

    else:
        print("Invalid choice!")