# This creates the Database for the warehouse management systems

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


db = sqlite3.connect("./database/database.db")
cur = db.cursor()

def createTables():
    try:
        # PALLET TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pallet(
                PalletID TEXT PRIMARY KEY NOT NULL,
                Dept TEXT NOT NULL,
                Class TEXT NOT NULL,
                Item TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                VCP INTEGER,
                SSP INTEGER,
                Size TEXT,
                StorageCode TEXT,
                Aisle TEXT,
                Bin TEXT,
                Level TEXT,
                ExpirationDate TEXT,
                Status TEXT,
                CreateDate TEXT,
                CreateID TEXT,
                PutDate TEXT,
                PutID TEXT,
                PullDate TEXT,
                PullID TEXT,
                FOREIGN KEY (Dept, Class, Item)
                    REFERENCES items(Dept, Class, Item),
                FOREIGN KEY (Aisle, Bin, Level)
                    REFERENCES locations(Aisle, Bin, Level),
                FOREIGN KEY (StorageCode)
                    REFERENCES storageCodes(StorageCode)
            )
        """)

        # ITEMS TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items(
                Dept TEXT NOT NULL,
                Class TEXT NOT NULL,
                Item TEXT NOT NULL,
                Name TEXT NOT NULL,
                Description TEXT NOT NULL, 
                StorageCode TEXT NOT NULL,
                VCP INTEGER NOT NULL,
                SSP INTEGER NOT NULL,
                Cost FLOAT NOT NULL,
                Price FLOAT NOT NULL,
                PRIMARY KEY (Dept, Class, Item),
                FOREIGN KEY (StorageCode)
                    REFERENCES storageCodes(StorageCode)
            )
        """)

        # STORAGECODES TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS storageCodes(
                StorageCode TEXT PRIMARY KEY,
                StorageType TEXT NOT NULL,
                Expire BOOLEAN NOT NULL,
                Restricted BOOLEAN NOT NULL
            )
        """)

        # LOCATIONS TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS locations(
                Aisle TEXT NOT NULL,
                Bin TEXT NOT NULL,
                Level TEXT NOT NULL,
                StorageCode TEXT NOT NULL,
                Size TEXT NOT NULL,
                Status TEXT NOT NULL,
                Zone TEXT NOT NULL,
                PRIMARY KEY (Aisle, Bin, Level),
                FOREIGN KEY (StorageCode)
                    REFERENCES storageCodes(StorageCode)
            )
        """)

        # USERS TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                UserID TEXT PRIMARY KEY,
                UserName TEXT NOT NULL,
                Password TEXT NOT NULL,
                Role TEXT NOT NULL,
                Department TEXT NOT NULL
            )
        """)

        # LABELS TABLE
        cur.execute("""
            CREATE TABLE IF NOT EXISTS labels(
                LabelID TEXT PRIMARY KEY,
                Aisle TEXT NOT NULL,
                Bin TEXT NOT NULL,
                Level TEXT NOT NULL,
                PalletID TEXT NOT NULL,
                Dept TEXT NOT NULL,
                Class TEXT NOT NULL,
                Item TEXT NOT NULL,
                PullQuant TEXT NOT NULL,
                Status TEXT NOT NULL,
                FOREIGN KEY (Dept, Class, Item)
                    REFERENCES items(Dept, Class, Item),
                FOREIGN KEY (Aisle, Bin, Level)
                    REFERENCES locations(Aisle, Bin, Level)
            )
        """)

        db.commit()
        messagebox.showinfo("Success", "All tables created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error creating tables:\n{e}")

def dropTable(tableName):
    try:
        cur.execute(f"DROP TABLE IF EXISTS {tableName}")
        db.commit()
    except Exception as e:
        messagebox.showerror("Error", f"Could not drop {tableName}:\n{e}")

def dropSelectedTables():
    selected = [name for name, var in checkboxes.items() if var.get()]
    if not selected:
        messagebox.showwarning("No Selection", "Please select at least one table to delete.")
        return

    confirm = messagebox.askyesno("Confirm", f"Delete the following tables?\n\n{', '.join(selected)}")
    if confirm:
        for name in selected:
            dropTable(name)
        messagebox.showinfo("Done", "Selected tables deleted successfully!")

def generateRandomData():
    # Placeholder for your later code
    messagebox.showinfo("Coming Soon", "Random data generation not implemented yet.")

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Warehouse Database Manager")
root.geometry("420x460")

# Apply ttk theme for macOS (clam or aqua works well)
style = ttk.Style()
style.theme_use("aqua")

# Custom styling
style.configure("TButton", padding=6, font=("Helvetica", 11))
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TCheckbutton", font=("Helvetica", 11))

# ---------- Layout ----------
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(main_frame, text="Warehouse Database Manager", font=("Helvetica", 16, "bold"))
title_label.pack(pady=(0, 15))

# Buttons
ttk.Button(main_frame, text="Create Tables", command=createTables).pack(pady=5, fill="x")

# Checkbox Section
frame = ttk.LabelFrame(main_frame, text="Delete Tables", padding=10)
frame.pack(pady=10, fill="x")

tables = ["storageCodes", "items", "locations", "pallet", "users", "labels"]
checkboxes = {}

for tbl in tables:
    var = tk.BooleanVar()
    checkboxes[tbl] = var
    ttk.Checkbutton(frame, text=tbl, variable=var).pack(anchor="w", pady=2)

ttk.Button(main_frame, text="Delete Selected Tables", command=dropSelectedTables).pack(pady=10, fill="x")

# Placeholder for Random Data button
ttk.Button(main_frame, text="Generate Random Data", command=generateRandomData).pack(pady=5, fill="x")

# Quit button (optional)
ttk.Button(main_frame, text="Exit", command=root.destroy).pack(pady=15, fill="x")

root.mainloop()