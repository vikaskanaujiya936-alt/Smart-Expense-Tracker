import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
from collections import defaultdict

FILE_NAME = "expenses.csv"


# ---------- DATA ----------

def load_expenses():
    try:
        with open(FILE_NAME, "r", newline="") as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(expenses)


# ---------- TOTAL ----------

def calculate_total():
    total = 0

    for row in load_expenses():
        if len(row) == 4:
            try:
                total += float(row[3])
            except ValueError:
                pass

    total_label.config(text=f"Total Expense\n₹ {total:.2f}")
def calculate_total():
    total = 0
    count = 0
    today_total = 0

    today = datetime.now().strftime("%d-%m-%Y")

    for row in load_expenses():
        if len(row) == 4:
            try:
                amount = float(row[3])

                total += amount
                count += 1

                if row[0] == today:
                    today_total += amount

            except ValueError:
                pass

    total_label.config(
        text=f"Total Expense\n₹ {total:.2f}"
    )

    count_label.config(
        text=f"Transactions\n{count}"
    )

    today_label.config(
        text=f"Today's Expense\n₹ {today_total:.2f}"
    )

# ---------- CATEGORY CHART ----------

def category_summary():
    summary = defaultdict(float)

    for row in load_expenses():
        if len(row) == 4:
            try:
                summary[row[2]] += float(row[3])
            except ValueError:
                pass

    return summary
def show_monthly_summary():

    expenses = load_expenses()

    monthly = defaultdict(float)

    for row in expenses:
        if len(row) == 4:
            try:
                date = datetime.strptime(
                    row[0],
                    "%d-%m-%Y"
                )

                month = date.strftime("%B %Y")

                monthly[month] += float(row[3])

            except ValueError:
                pass

    if not monthly:
        messagebox.showinfo(
            "Monthly Summary",
            "No expense data available."
        )
        return

    summary_window = tk.Toplevel(root)

    summary_window.title(
        "Monthly Expense Summary"
    )

    summary_window.geometry(
        "450x450"
    )

    tk.Label(
        summary_window,
        text="MONTHLY EXPENSE SUMMARY",
        font=("Arial", 18, "bold")
    ).pack(pady=20)

    for month, amount in monthly.items():

        tk.Label(
            summary_window,
            text=f"{month}  →  ₹ {amount:.2f}",
            font=("Arial", 13)
        ).pack(pady=8)

def show_category_chart():

    summary = category_summary()

    if not summary:
        messagebox.showinfo(
            "Chart",
            "No expense data available."
        )
        return

    chart_window = tk.Toplevel(root)

    chart_window.title(
        "Category-wise Expense"
    )

    chart_window.geometry(
        "650x500"
    )

    tk.Label(
        chart_window,
        text="CATEGORY-WISE EXPENSE",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    canvas = tk.Canvas(
        chart_window,
        width=600,
        height=350,
        bg="white"
    )

    canvas.pack()

    max_amount = max(summary.values())

    x = 60
    bar_width = 70

    for category, amount in summary.items():

        bar_height = (
            amount / max_amount
        ) * 250

        canvas.create_rectangle(
            x,
            300 - bar_height,
            x + bar_width,
            300
        )

        canvas.create_text(
            x + bar_width / 2,
            320,
            text=category[:10]
        )

        canvas.create_text(
            x + bar_width / 2,
            285 - bar_height,
            text=f"₹{amount:.0f}"
        )

        x += 110

        if x > 550:
            break


# ---------- TABLE ----------

def refresh_table():

    for item in table.get_children():
        table.delete(item)

    expenses = load_expenses()

    for i, row in enumerate(expenses):

        if len(row) == 4:

            table.insert(
                "",
                "end",
                iid=str(i),
                values=(
                    row[0],
                    row[1],
                    row[2],
                    "₹ " + row[3]
                )
            )

    calculate_total()


# ---------- ADD ----------

def add_expense():

    name = name_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_entry.get().strip()

    if not name or not amount or not category:

        messagebox.showwarning(
            "Missing Information",
            "Please fill all fields."
        )

        return

    try:

        amount = float(amount)

        if amount <= 0:
            raise ValueError

    except ValueError:

        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid positive number."
        )

        return

    date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    with open(
        FILE_NAME,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [date, name, category, amount]
        )

    name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)

    refresh_table()

    messagebox.showinfo(
        "Success",
        "Expense added successfully!"
    )


# ---------- DELETE ----------
def delete_expense():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Expense",
            "Please select an expense first."
        )
        return

    index = int(selected[0])

    expenses = load_expenses()

    if 0 <= index < len(expenses):

        deleted = expenses.pop(index)

        save_expenses(expenses)

        refresh_table()

        messagebox.showinfo(
            "Deleted",
            f"{deleted[1]} deleted successfully!"
        )
def edit_expense():

    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Expense",
            "Please select an expense first."
        )
        return

    index = int(selected[0])

    expenses = load_expenses()

    if index >= len(expenses):
        return

    old_data = expenses[index]

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Expense")
    edit_window.geometry("400x350")
    edit_window.resizable(False, False)

    tk.Label(
        edit_window,
        text="EDIT EXPENSE",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    tk.Label(
        edit_window,
        text="Expense Name"
    ).pack()

    edit_name = tk.Entry(
        edit_window,
        width=30
    )
    edit_name.pack(pady=5)
    edit_name.insert(0, old_data[1])

    tk.Label(
        edit_window,
        text="Amount"
    ).pack()

    edit_amount = tk.Entry(
        edit_window,
        width=30
    )
    edit_amount.pack(pady=5)
    edit_amount.insert(0, old_data[3])

    tk.Label(
        edit_window,
        text="Category"
    ).pack()

    edit_category = ttk.Combobox(
        edit_window,
        values=[
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Education",
            "Entertainment",
            "Medical",
            "Other"
        ],
        width=27,
        state="readonly"
    )

    edit_category.pack(pady=5)

    if old_data[2] in edit_category["values"]:
        edit_category.set(old_data[2])
    else:
        edit_category.set("Other")

    def save_changes():

        new_name = edit_name.get().strip()
        new_amount = edit_amount.get().strip()
        new_category = edit_category.get().strip()

        if not new_name or not new_amount or not new_category:
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields.",
                parent=edit_window
            )
            return

        try:
            new_amount = float(new_amount)

            if new_amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount.",
                parent=edit_window
            )
            return

        expenses[index] = [
            old_data[0],
            new_name,
            new_category,
            new_amount
        ]

        save_expenses(expenses)
        refresh_table()

        edit_window.destroy()

        messagebox.showinfo(
            "Updated",
            "Expense updated successfully!"
        )

    tk.Button(
        edit_window,
        text="Save Changes",
        command=save_changes,
        width=20
    ).pack(pady=20)

# ---------- EXPORT ----------

def export_expenses():

    expenses = load_expenses()

    if not expenses:
        messagebox.showinfo(
            "Export",
            "No expenses available to export."
        )
        return

    export_file = "expenses_export.csv"

    with open(export_file, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Date",
            "Expense Name",
            "Category",
            "Amount"
        ])

        writer.writerows(expenses)

    messagebox.showinfo(
        "Export Successful",
        f"Expenses exported successfully!\n\nFile: {export_file}"
    )
# ---------- SHOW ALL ----------

def show_all():

    search_entry.delete(0, tk.END)

    refresh_table()
# ---------- SEARCH ----------
def search_expense():

    keyword = search_entry.get().strip().lower()

    for item in table.get_children():
        table.delete(item)

    expenses = load_expenses()

    if keyword == "":
        refresh_table()
        return

    found = False

    for i, row in enumerate(expenses):

        if len(row) == 4:

            name = row[1].lower()
            category = row[2].lower()

            if keyword in name or keyword in category:

                table.insert(
                    "",
                    "end",
                    iid=str(i),
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        "₹ " + row[3]
                    )
                )

                found = True

    if not found:
        messagebox.showinfo(
            "Search",
            f"No expense found for '{keyword}'."
        )
# ---------- MAIN WINDOW ----------
root = tk.Tk()
root.title("Smart Expense Tracker | Expense Management System")

root.geometry("950x700")

root.resizable(False, False)
# ---------- DASHBOARD ----------
dashboard = tk.Frame(root)
dashboard.pack(pady=15)
title_label = tk.Label(
    root,
    text="💰 SMART EXPENSE TRACKER",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=10)
total_label = tk.Label(
    dashboard,
    text="Total Expense\n₹ 0.00",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=15,
    relief="groove",
    borderwidth=2
)
count_label = tk.Label(
    dashboard,
    text="Total Entries\n0",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=15,
    relief="groove",
    borderwidth=2
)
today_label = tk.Label(
    dashboard,
    text="Today's Expense\n₹ 0.00",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=15,
    relief="groove",
    borderwidth=2
)
total_label.grid(row=0, column=0, padx=20, pady=10)
count_label.grid(row=0, column=1, padx=20, pady=10)
today_label.grid(row=0, column=2, padx=20, pady=10)
# ---------- BUDGET STATUS ----------

def show_budget_status():

    expenses = load_expenses()

    try:
        with open("budget.txt", "r") as file:
            budget = float(file.read())

    except FileNotFoundError:
        messagebox.showinfo(
            "Budget",
            "Please set your monthly budget first."
        )
        return

    total_spent = 0

    for row in expenses:

        if len(row) == 4:

            try:
                total_spent += float(row[3])

            except ValueError:
                pass

    remaining = budget - total_spent

    if remaining >= 0:

        status = (
            f"Monthly Budget: ₹{budget:.2f}\n\n"
            f"Total Spent: ₹{total_spent:.2f}\n\n"
            f"Remaining: ₹{remaining:.2f}"
        )

    else:

        status = (
            f"Monthly Budget: ₹{budget:.2f}\n\n"
            f"Total Spent: ₹{total_spent:.2f}\n\n"
            f"⚠️ Budget Exceeded: ₹{abs(remaining):.2f}"
        )

    messagebox.showinfo(
        "Budget Status",
        status
    )
# ---------- SET BUDGET ----------

def set_budget():

    budget_window = tk.Toplevel(root)

    budget_window.title("Set Monthly Budget")
    budget_window.geometry("350x250")

    tk.Label(
        budget_window,
        text="SET MONTHLY BUDGET",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        budget_window,
        text="Enter Budget Amount:"
    ).pack()

    budget_entry = tk.Entry(
        budget_window,
        width=25
    )

    budget_entry.pack(pady=10)

    def save_budget():

        try:
            budget = float(budget_entry.get())

            if budget <= 0:
                raise ValueError

            with open("budget.txt", "w") as file:
                file.write(str(budget))

            messagebox.showinfo(
                "Budget Saved",
                f"Monthly budget set to ₹{budget:.2f}"
            )

            budget_window.destroy()

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid budget."
            )

    tk.Button(
        budget_window,
        text="Save Budget",
        command=save_budget,
        width=15
    ).pack(pady=15)


# ---------- DASHBOARD BUTTONS ----------

chart_button = tk.Button(
    dashboard,
    text="📊 Category Chart",
    command=show_category_chart,
    width=18,
    height=2,
    relief="raised",
    borderwidth=2,
    font=("Arial", 10, "bold"),
    cursor="hand2"
)

chart_button.grid(
    row=1,
    column=0,
    padx=10,
    pady=15
)


monthly_button = tk.Button(
    dashboard,
    text="📅 Monthly Summary",
    command=show_monthly_summary,
    width=18,
    height=2,
    relief="raised",
    borderwidth=2,
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
monthly_button.grid(
    row=1,
    column=1,
    padx=10,
    pady=15
)


budget_button = tk.Button(
    dashboard,
    text="💰 Set Budget",
    command=set_budget,
    width=20,
    height=3,
    relief="raised",
    borderwidth=2,
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
budget_button.grid(
    row=1,
    column=2,
    padx=10,
    pady=15
)
budget_status_button = tk.Button(
    dashboard,
    text="📊 Budget Status",
    command=show_budget_status,
    width=20,
    height=3,
    relief="raised",
    borderwidth=2,
    font=("Arial", 10, "bold"),
    cursor="hand2"
)


budget_status_button.grid(
    row=2,
    column=1,
    padx=10,
    pady=5
)

# ---------- INPUT ----------

input_frame = tk.Frame(root)

input_frame.pack(
    pady=10
)


tk.Label(
    input_frame,
    text="Expense Name"
).grid(
    row=0,
    column=0,
    padx=5
)


name_entry = tk.Entry(
    input_frame,
    width=18
)

name_entry.grid(
    row=1,
    column=0,
    padx=5
)


tk.Label(
    input_frame,
    text="Amount"
).grid(
    row=0,
    column=1,
    padx=5
)


amount_entry = tk.Entry(
    input_frame,
    width=15
)

amount_entry.grid(
    row=1,
    column=1,
    padx=5
)


tk.Label(
    input_frame,
    text="Category"
).grid(
    row=0,
    column=2,
    padx=5
)


category_entry = ttk.Combobox(
    input_frame,
    values=[
        "Food",
        "Travel",
        "Shopping",
        "Bills",
        "Education",
        "Entertainment",
        "Medical",
        "Other"
    ],
    width=16,
    state="readonly"
)

category_entry.grid(
    row=1,
    column=2,
    padx=5
)

category_entry.set("Select Category")

add_button = tk.Button(
    input_frame,
    text="Add Expense",
    command=add_expense,
    width=15
)

add_button.grid(
    row=1,
    column=3,
    padx=10
)


# ---------- SEARCH ----------

search_frame = tk.Frame(root)

search_frame.pack(
    pady=15
)


tk.Label(
    search_frame,
    text="Search:"
).pack(
    side=tk.LEFT
)


search_entry = tk.Entry(
    search_frame,
    width=30
)

search_entry.pack(
    side=tk.LEFT,
    padx=5
)


search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_expense
)

search_button.pack(
    side=tk.LEFT,
    padx=5
)
export_button = tk.Button(
    search_frame,
    text="📁 Export CSV",
    command=export_expenses,
    width=15
)

export_button.pack(
    side=tk.LEFT,
    padx=5
)

show_button = tk.Button(
    search_frame,
    text="Show All",
    command=show_all
)

show_button.pack(
    side=tk.LEFT
)
# ---------- TABLE ----------

columns = (
    "Date",
    "Expense Name",
    "Category",
    "Amount"
)


table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=14
)


for column in columns:

    table.heading(
        column,
        text=column
    )


table.column(
    "Date",
    width=150
)

table.column(
    "Expense Name",
    width=250
)

table.column(
    "Category",
    width=200
)

table.column(
    "Amount",
    width=180
)


table.pack(
    pady=10
)
# ---------- BUTTONS ----------

bottom_frame = tk.Frame(root)

bottom_frame.pack(
    pady=10
)


edit_button = tk.Button(
    bottom_frame,
    text="✏ Edit Selected",
    command=edit_expense,
    width=18
)

edit_button.pack(
    side=tk.LEFT,
    padx=5
)


delete_button = tk.Button(
    bottom_frame,
    text="🗑 Delete Selected",
    command=delete_expense,
    width=18
)

delete_button.pack(
    side=tk.LEFT,
    padx=5
)


refresh_button = tk.Button(
    bottom_frame,
    text="Refresh",
    command=refresh_table,
    width=12
)

refresh_button.pack(
    side=tk.LEFT,
    padx=5
)


# ---------- START ----------

refresh_table()

root.mainloop()