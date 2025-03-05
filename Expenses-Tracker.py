import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL,
        category TEXT,
        description TEXT
    )
""")
conn.commit()

# Functions
def add_expense():
    try:
        amount = float(amount_entry.get())
        category = category_var.get()
        description = desc_entry.get("1.0", tk.END).strip()

        if not description:
            description = "No Description"

        cursor.execute("INSERT INTO expenses (amount, category, description) VALUES (?, ?, ?)", 
                       (amount, category, description))
        conn.commit()
        messagebox.showinfo("Success", "Expense Added!")

        # **Clear input fields after adding**
        amount_entry.delete(0, tk.END)
        desc_entry.delete("1.0", tk.END)

        display_expenses()
    except ValueError:
        messagebox.showerror("Error", "Invalid Amount!")

def display_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    expense_list.delete(0, tk.END)
    total = 0
    for row in rows:
        expense_list.insert(tk.END, f"ID: {row[0]} | ₹{row[1]} | {row[2]} | {row[3]}")
        total += row[1]
    total_label.config(text=f"Total Spent: ₹{total}")

def delete_expense():
    selected = expense_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Select an expense to delete!")
        return

    expense_id = expense_list.get(selected[0]).split("|")[0].split(":")[1].strip()
    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Expense Deleted!")
    display_expenses()

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("500x500")

# Amount Entry
tk.Label(root, text="Amount (₹)").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Category Dropdown
tk.Label(root, text="Category").pack()
category_var = tk.StringVar(value="Food")
tk.OptionMenu(root, category_var, "Food", "Transport", "Shopping", "Rent", "Other").pack()

# Description Entry
tk.Label(root, text="Description").pack()
desc_entry = tk.Text(root, height=2, width=40)
desc_entry.pack()

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="Delete Expense", command=delete_expense).pack(pady=5)

# Expense Listbox
tk.Label(root, text="Expense History").pack()
expense_list = tk.Listbox(root, width=60, height=10)
expense_list.pack()

# Total Spent Label
total_label = tk.Label(root, text="Total Spent: ₹0", font=("Arial", 12, "bold"))
total_label.pack()

# Display Initial Expenses
display_expenses()

# Run App
root.mainloop()
S
