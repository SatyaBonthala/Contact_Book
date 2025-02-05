import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import csv
import ttkbootstrap as tb  # Import ttkbootstrap for better UI

# File to store contacts
FILE_NAME = "contacts.csv"

# Create file if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email"])

# Function to add a new contact
def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()

    if not name or not phone or not email:
        messagebox.showerror("Error", "All fields are required!")
        return

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, phone, email])

    messagebox.showinfo("Success", "Contact added successfully!")
    clear_fields()
    load_contacts()

# Function to load contacts into the table
def load_contacts():
    for row in tree.get_children():
        tree.delete(row)

    try:
        df = pd.read_csv(FILE_NAME)
        for index, row in df.iterrows():
            tree.insert("", "end", values=(row["Name"], row["Phone"], row["Email"]))
    except pd.errors.EmptyDataError:
        pass

# Function to search contacts
def search_contact():
    query = search_var.get().strip().lower()
    if not query:
        messagebox.showerror("Error", "Please enter a name or phone number to search!")
        return

    for row in tree.get_children():
        tree.delete(row)

    df = pd.read_csv(FILE_NAME)
    filtered = df[df.apply(lambda x: query in str(x).lower(), axis=1)]
    
    if not filtered.empty:
        for index, row in filtered.iterrows():
            tree.insert("", "end", values=(row["Name"], row["Phone"], row["Email"]))
    else:
        messagebox.showinfo("Not Found", "No matching contact found!")

# Function to delete selected contact
def delete_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a contact to delete!")
        return

    contact = tree.item(selected)["values"]
    name, phone, email = contact

    df = pd.read_csv(FILE_NAME)
    df = df[(df["Name"] != name) | (df["Phone"] != phone) | (df["Email"] != email)]
    df.to_csv(FILE_NAME, index=False)

    messagebox.showinfo("Success", "Contact deleted successfully!")
    load_contacts()

# Function to clear input fields
def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")

# GUI Setup using ttkbootstrap
root = tb.Window(themename="darkly")  # Set a modern theme
root.title("📞 Contact Book")
root.geometry("600x600")

# Style
style = ttk.Style()
style.configure("Treeview", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TEntry", font=("Arial", 12))

# Input Fields
name_var = tk.StringVar()
phone_var = tk.StringVar()
email_var = tk.StringVar()
search_var = tk.StringVar()

frame = ttk.Frame(root, padding=10)
frame.pack(pady=10, fill="x")

ttk.Label(frame, text="Name:", font=("Arial", 12), foreground="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
ttk.Entry(frame, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=5)

ttk.Label(frame, text="Phone:", font=("Arial", 12), foreground="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
ttk.Entry(frame, textvariable=phone_var, width=30).grid(row=1, column=1, padx=10, pady=5)

ttk.Label(frame, text="Email:", font=("Arial", 12), foreground="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
ttk.Entry(frame, textvariable=email_var, width=30).grid(row=2, column=1, padx=10, pady=5)

ttk.Button(frame, text="Add Contact", command=add_contact, bootstyle="success").grid(row=3, column=0, columnspan=2, pady=10)

# Search Bar
search_frame = ttk.Frame(root, padding=10)
search_frame.pack(fill="x")

ttk.Label(search_frame, text="Search by Name or Phone:", font=("Arial", 12), foreground="white").pack(pady=5)
ttk.Entry(search_frame, textvariable=search_var, width=30).pack(pady=2)
ttk.Button(search_frame, text="Search", command=search_contact, bootstyle="primary").pack(pady=5)

# Contact Table
table_frame = ttk.Frame(root, padding=10)
table_frame.pack(fill="both", expand=True)

columns = ("Name", "Phone", "Email")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview")

tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Email", text="Email")
tree.pack(pady=10, fill="both", expand=True)

# Delete Button
ttk.Button(root, text="Delete Contact", command=delete_contact, bootstyle="danger").pack(pady=10)

# Load Contacts on Start
load_contacts()

# Run the Application
root.mainloop()
