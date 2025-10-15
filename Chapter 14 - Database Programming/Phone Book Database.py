'''
Write a program that creates a database named phonebook.db. 
The database should have a table named Entries, 
with columns for a person’s name and phone number. 
Next, write a CRUD application that lets the user add rows to the Entries table, 
look up a person’s phone number, 
change a person’s phone number, 
and delete specified rows.
'''

import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re

# Creates or connectes to database and creates a cursor
db = sqlite3.connect("phonebook.db")
cur = db.cursor()

# Creates the Table, destroying the table if it already exists
cur.execute("""DROP TABLE IF EXISTS Entries""")
cur.execute("""CREATE TABLE IF NOT EXISTS Entries(
            Name TEXT,
            Phone TEXT
            )""")

# Create a base database to use, comment out for an empty database
phone_database = [('Breutzmann, Robert', '319-939-3687'),
                  ('Bradley, Brenda', '319-231-9814'),
                  ('Blomgren, Josh', '319-541-9853'),
                  ('Lubeck, Jamie', '555-986-8841'),
                  ('Willson, Samantha', '555-555-1436'),
                  ('Greenfield, Amara', '468-826-6871')
                  ]
for row in phone_database:
    cur.execute("""INSERT INTO Entries(Name, Phone) VALUES (?,?)""", (row[0], row[1]))


# Validates the phone number is in a valid format.
def is_valid_phone(phone):
    pattern = r"^\d{3}-\d{3}-\d{4}$"
    return re.match(pattern, phone) is not None

# Validates the name is in a valid format.
def is_valid_name(name):
    pattern = r"^[A-Za-z][A-Za-z\s\-]*,\s*[A-Za-z][A-Za-z\s\-]*$"
    return re.match(pattern, name) is not None

### Create the Functions to interact with the table

# Adds an Entry to the Database
def add_db():
    if is_valid_phone(phone.get()) == False:
        messagebox.showerror("Invalid Input", "Phone number must be in the format ###-###-####.")
    elif is_valid_name(name.get()) == False:
        messagebox.showerror("Invalid Input", "Name must be entered as 'Last, First.'")
    else:
        cur.execute(
        """INSERT INTO Entries(Name, Phone) VALUES (?,?)""",
        (name.get(), phone.get()))
        messagebox.showinfo("Success", f"Entry added:\nName: {name.get()}\nPhone: {phone.get()}")

# Edits an Entry in the Database
def edit_db():
    # Create Local Variables
    newname = changeName.get()
    newphone = changePhone.get()
    curname = name.get()
    curphone = phone.get()
    noNameChanges = newname == "" or newname == curname
    noPhoneChanges = newphone == "" or newphone == curphone

    # Checks for errors in entries
    if newname != "" and is_valid_name(newname) == False:
        messagebox.showerror("Invalid Input", "Name must be entered as 'Last, First.'")
        return
    elif newphone !="" and is_valid_phone(newphone) == False:
        messagebox.showerror("Invalid Input", "Phone number must be in the format ###-###-####.")
        return
    elif noNameChanges and noPhoneChanges:
        messagebox.showerror("Invalid Input", "No changes detected")
        return
    
    # Commits Changes
    if not noPhoneChanges and noNameChanges:
        cur.execute("""UPDATE Entries SET Phone = ? WHERE Name = ?""", (newphone, curname))
        messagebox.showinfo("Success", f"Entry updated:\nName: {curname}\nUpdated Phone: {newphone}")
    elif not noNameChanges and noPhoneChanges:
        cur.execute("""UPDATE Entries SET Name = ? WHERE Name = ?""", (newname, curname))
        messagebox.showinfo("Success", f"Entry updated:\nUpdated Name: {newname}\nPhone: {curphone}")
    elif not noNameChanges and not noPhoneChanges:
        cur.execute("""UPDATE Entries SET Name = ?, Phone = ? WHERE Name = ?""", (newname, newphone, curname))
        messagebox.showinfo("Success", f"Entry updated:\nUpdated Name: {newname}\nUpdated Phone: {newphone}")

# Delete entry from Database
def delete_db():
    curname = name.get()
    curphone = phone.get()
    response = messagebox.askokcancel("Are you sure?", f"You are about to delete this entry! \nName: {curname}\nPhone: {curphone}\nAre you sure?")
    if response == True:
        cur.execute("""DELETE FROM Entries WHERE name = ?""", (curname,))
        messagebox.showinfo("Success", f"Entry deleted:\nName: {curname}\nPhone: {curphone}")
    else:
        messagebox.showinfo("Canceled", f"Entry Deletion Canceled!")


### Create the GUI for the CRUD application

# Create the Main Window with the options.å
root = tk.Tk()
root.title("Main Menu")
root.geometry("+600+400")

# Create Variables for the GUI
name = tk.StringVar()
phone = tk.StringVar()
changeName = tk.StringVar()
changePhone = tk.StringVar()

## Create functions for each button

# Add Entry
def add_entry():
    win = tk.Toplevel()
    win.title("Add an Entry")
    name.set("Doe, John")
    phone.set("123-456-7890")
    
    nameLabel = tk.Label(win, text="Enter Name (Last, First)")
    nameLabel.grid(column=0, row=0)
    phoneLabel = tk.Label(win, text="Enter Phone Number (xxx-xxx-xxxx)")
    phoneLabel.grid(column=1, row=0)
    
    nameEntry = tk.Entry(win, textvariable=name, width=30)
    nameEntry.grid(column=0, row=1)
    phoneEntry = tk.Entry(win, textvariable=phone, width=30)
    phoneEntry.grid(column=1, row=1)

    submitButton = tk.Button(win, text="Submit", command=lambda: (add_db(), win.destroy()))
    submitButton.grid(column=0, row=2)
    cancelButton = tk.Button(win, text="Return to Main Menu", command=win.destroy)
    cancelButton.grid(column=1, row=2)

# Lookup Entry Popup
def lookup_entry():
    # Gets all the names from the database, creates a dictionary
    cur.execute("SELECT Name, Phone FROM Entries")
    entries = cur.fetchall()
    name_to_phone = {name: phone for name, phone in entries}
    names = list(name_to_phone.keys())

    win = tk.Toplevel()
    win.title("Phone Number Lookup")
    # Tkinter variable to hold the selected name
    selected_name = tk.StringVar()
    selected_name.set(names[0] if names else "")

    # Label to display phone number
    phone_label = tk.Label(win, text=name_to_phone.get(selected_name.get(), ""), width=30)
    phone_label.grid(column=1, row=0, pady=10)

    # Function to update phone label whenever selection changes
    def update_phone(*args):
        phone_label.config(text=name_to_phone.get(selected_name.get(), ""))

    selected_name.trace_add("write", update_phone)

    # Create dropdown
    dropdown = tk.OptionMenu(win, selected_name, *names)
    dropdown.grid(column=0, row=0, pady=10)

    # Create a cancil button
    cancelButton = tk.Button(win, text="Return to Main Menu", command=win.destroy)
    cancelButton.grid(column=0, row=1, columnspan=2)


# Edit Entry Popup
def edit_entry():
        # Gets all the names from the database, creates a dictionary
    cur.execute("SELECT Name, Phone FROM Entries")
    entries = cur.fetchall()
    name_to_phone = {name: phone for name, phone in entries}
    names = list(name_to_phone.keys())

    win = tk.Toplevel()
    win.title("Edit an Entry")

    # Tkinter variable to hold the selected name and phone
    name.set(names[0] if names else "")
    phone.set(name_to_phone.get(name.get(), "")) 

    # Label to display phone number
    phone_label = tk.Label(win, textvariable=phone, width=30)
    phone_label.grid(column=1, row=0, pady=10)

    # Function to update phone label whenever selection changes
    def update_phone(*args):
        phone.set(name_to_phone.get(name.get(), ""))

    name.trace_add("write", update_phone)

    # Create dropdown
    dropdown = tk.OptionMenu(win, name, *names)
    dropdown.grid(column=0, row=0, pady=10)

    # Create the entry fields and labels to edit the entry
    changeNameLabel = tk.Label(win, text="Change Name to (Leave blank to keep)", width=30)
    changeNameLabel.grid(column=0, row=1, sticky="s", pady=10)
    changePhoneLabel = tk.Label(win, text="Chane Phone to (leave blank to keep)", width=30)
    changePhoneLabel.grid(column=1, row=1, pady=10, sticky="s")
    changeNameEntry = tk.Entry(win, textvariable=changeName)
    changeNameEntry.grid(column=0, row=2)
    changePhoneEntry = tk.Entry(win, textvariable=changePhone)
    changePhoneEntry.grid(column=1, row=2)


    # Create a button
    submitButton = tk.Button(win, text="Submit", command=lambda: (edit_db(), win.destroy()))
    submitButton.grid(column=0, row=3)
    cancelButton = tk.Button(win, text="Return to Main Menu", command=win.destroy)
    cancelButton.grid(column=1, row=3)

# Delete Entry Popup
def delete_entry():
     # Gets all the names from the database, creates a dictionary
    cur.execute("SELECT Name, Phone FROM Entries")
    entries = cur.fetchall()
    name_to_phone = {name: phone for name, phone in entries}
    names = list(name_to_phone.keys())

    win = tk.Toplevel()
    win.title("Delete an Entry")

    name.set(names[0] if names else "")
    phone.set(name_to_phone.get(name.get(), "")) 

    # Label to display phone number
    phone_label = tk.Label(win, textvariable=phone, width=30)
    phone_label.grid(column=1, row=0, pady=10)

    # Function to update phone label whenever selection changes
    def update_phone(*args):
        phone.set(name_to_phone.get(name.get(), "")) 

    name.trace_add("write", update_phone)

    # Create dropdown
    dropdown = tk.OptionMenu(win, name, *names)
    dropdown.grid(column=0, row=0, pady=10)

    # Create a delete and cancel button
    deleteButton = tk.Button(win, text="Delete Entry", command=lambda: (delete_db(), win.destroy()))
    deleteButton.grid(column=0, row=1)
    cancelButton = tk.Button(win, text="Return to Main Menu", command=win.destroy)
    cancelButton.grid(column=1, row=1)

# Create and Pack the buttons to open the other windows
addButton = tk.Button(root, text="Add an entry", command=add_entry).pack()
lookupButton = tk.Button(root, text="Look up an entry", command=lookup_entry).pack()
editButton = tk.Button(root, text="Edit an entry", command=edit_entry).pack()
deleteButton = tk.Button(root, text="Delete an entry", command=delete_entry).pack()
quitButton = tk.Button(root, text="Exit Program", command=root.destroy).pack()

root.mainloop()
db.commit()