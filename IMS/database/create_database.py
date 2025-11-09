# This creates the Database for the warehouse management systems

import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
from datetime import datetime
import pandas as pd

db_path = "IMS/database/database.db"
db = sqlite3.connect(db_path)
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

def populate_storageCodes():
    """Create the storage_codes table and populate it with default values."""
    try:
        db = sqlite3.connect(db_path)
        cur = db.cursor()

        # Create table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS storageCodes (
                StorageCode TEXT PRIMARY KEY,
                StorageType TEXT NOT NULL,
                Expire BOOLEAN NOT NULL,
                Restricted BOOLEAN NOT NULL
            )
        """)

        # Default storage codes
        storage_data = [
            ('CR', 'Conveyable Reserve', 0, 0),
            ('FD', 'Food', 1, 0),
            ('NC', 'Non-Conveyable', 0, 0),
            ('NF', 'Non-Conveyable Food', 1, 0),
            ('RS', 'Restricted Reserve', 0, 1),
            ('RF', 'Restricted Food', 1, 1),
            ('BS', 'Security', 0, 1),
        ]

        # Insert or ignore to prevent duplicates
        cur.executemany("""
            INSERT OR IGNORE INTO storageCodes (StorageCode, StorageType, Expire, Restricted)
            VALUES (?, ?, ?, ?)
        """, storage_data)

        db.commit()
        messagebox.showinfo("Success", "Storage Codes generated successfully!")

    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to generate storage codes:\n{e}")

def populate_items():
    try:
        db = sqlite3.connect(db_path)
        cur = db.cursor()
        # Ensure storageCodes table has values
        cur.execute("SELECT COUNT(*) FROM storageCodes")
        count = cur.fetchone()[0]
        if count == 0:
            messagebox.showerror("Missing Data", "Please populate Storage Codes before adding items.")
            return

        # Clear out existing items first (optional reset)
        cur.execute("DELETE FROM items")

        # Define departments and their type behavior
        departments = {
            "100": {"name": "Non-Food", "storageCodes": ["CR", "NC"]},
            "200": {"name": "Food", "storageCodes": ["FD", "NF"]},
            "300": {"name": "Security", "storageCodes": ["BS"]},
            "400": {"name": "Restricted", "storageCodes": ["RS", "RF"]}
        }

        classes = ["01", "02", "03", "04"]

        # Example items per class
        sample_items = [
            "Paper Towels", "Toilet Paper", "Laundry Detergent", "Diapers",
            "Cereal", "Pasta Sauce", "Soda 12-pack", "Chips",
            "Laptop", "Headphones", "Bluetooth Speaker", "Game Console",
            "Bleach", "Motor Oil", "Batteries", "Drain Cleaner"
        ]

        for dept_code, dept_info in departments.items():
            for class_code in classes:
                for i in range(1, 11):
                    item_code = f"{i:04d}"

                    # Generate item name
                    base_name = random.choice(sample_items)
                    item_name = f"{base_name} {dept_code}{class_code}{item_code}"[:30]

                    # Description
                    description = f"{base_name} from department {dept_info['name']}"

                    # Assign a storage code from department type
                    storage_code = random.choice(dept_info["storageCodes"])

                    # VCP/SSP (case quantity)
                    vcp = ssp = random.choice([1, 6, 12, 24])

                    # Random cost
                    cost = round(random.uniform(2.0, 100.0), 2)

                    # Price: 30% markup, rounded to nearest $5 minus a cent
                    raw_price = cost * 1.3
                    rounded_price = round(raw_price / 5) * 5 - 0.01

                    cur.execute("""
                        INSERT INTO items (Dept, Class, Item, Name, Description, StorageCode, VCP, SSP, Cost, Price)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (dept_code, class_code, item_code, item_name, description,
                          storage_code, vcp, ssp, cost, rounded_price))

        db.commit()
        messagebox.showinfo("Success", "Items table populated successfully!")

    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to populate items:\n{e}")

def populate_locations():
    """
    Populates the Locations table with a fixed warehouse layout.
    All locations start with Status='Empty'.
    """
    db = sqlite3.connect(db_path)
    cur = db.cursor()
    aisle_start = 300  # Starting aisle number
    bins_per_aisle = 128

    # Helper function to assign zone based on bin
    def get_zone(bin_num):
        if bin_num > 96:
            return 1
        elif bin_num > 64:
            return 2
        elif bin_num > 32:
            return 3
        else:
            return 4

    # Define aisle layouts: (StorageCode, levels, level_sizes)
    aisle_layouts = [
        # CR aisles
        ("CR", 10, ["M"] + ["HS"]*9),
        ("CR", 8, ["M"] + ["S"]*7),
        ("CR", 6, ["M"]*6),
        ("CR", 5, ["M"] + ["L"]*4),

        # FD aisles
        ("FD", 10, ["M"] + ["HS"]*9),
        ("FD", 8, ["M"] + ["S"]*7),
        ("FD", 6, ["M"]*6),
        ("FD", 5, ["M"] + ["L"]*4),

        # NC aisles
        ("NC", 6, ["M", "L", "L", "S", "S", "S"]),
        ("NC", 8, ["M"]*4 + ["HS"]*4),

        # NF aisles
        ("NF", 6, ["M", "L", "L", "S", "S", "S"]),
        ("NF", 8, ["M"]*4 + ["HS"]*4),

        # RS/RF aisle
        ("RS_RF", 8, ["L", "L", "M", "S", "S", "HS", "HS", "M"]),

        # BS aisle
        ("BS", 8, ["L", "L", "M", "S", "S", "HS", "HS", "M"]),
    ]

    for layout in aisle_layouts:
        storage_code, num_levels, level_sizes = layout
        aisle_number = aisle_start
        aisle_start += 1  # increment aisle for next layout

        for bin_num in range(1, bins_per_aisle + 1):
            for level in range(1, num_levels + 1):
                size = level_sizes[level - 1]

                # Determine zone (RS_RF aisle has special zone rules)
                if storage_code == "RS_RF":
                    if bin_num > 96:
                        zone = 1
                    elif bin_num > 64:
                        zone = 2
                    elif bin_num > 32:
                        zone = 3
                    else:
                        zone = 4
                    # Optionally assign RS/RF based on zone (e.g., RS = zones 1-2, RF = zones 3-4)
                    actual_storage_code = "RS" if zone in (1, 2) else "RF"
                else:
                    zone = get_zone(bin_num)
                    actual_storage_code = storage_code

                cur.execute("""
                    INSERT INTO locations (Aisle, Bin, Level, StorageCode, Size, Status, Zone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (str(aisle_number), bin_num, level, actual_storage_code, size, "Empty", str(zone)))

    db.commit()
    messagebox.showinfo("Success", "Locations populated successfully!")

ISO_NOW = datetime.now().isoformat(sep=' ', timespec='seconds')

def random_pallet_id(cur):
    import random
    while True:
        pid = f"{random.randint(10000000, 99999999)}"  # 8-digit number as string
        cur.execute("SELECT 1 FROM pallet WHERE PalletID=?", (pid,))
        if not cur.fetchone():
            return pid

def random_quantity(vcp=6):
    """Return a random quantity, typically a multiple of VCP."""
    multiples = [1, 2, 3, 4, 6, 12, 24]
    return random.choice(multiples) * vcp

def populate_pallets(fill_percent=0.9, created_by=1):
    db = sqlite3.connect(db_path)
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    # Get all empty locations
    cur.execute("SELECT * FROM locations WHERE Status='Empty'")
    locations = cur.fetchall()
    total_locations = len(locations)
    target_fill = int(total_locations * fill_percent)
    filled = 0

    # Get all items
    cur.execute("SELECT Dept, Class, Item, StorageCode, VCP, SSP FROM items")
    items = cur.fetchall()

    if not locations or not items:
        print("No locations or items to populate.")
        return

    for loc in locations:
        if filled >= target_fill:
            break

        # Pick random item
        item = random.choice(items)
        
        # Generate pallet attributes
        pallet_id = random_pallet_id(cur)
        dept, cls, item_code = item["Dept"], item["Class"], item["Item"]
        vcp, ssp = item["VCP"], item["SSP"]
        qty = random_quantity(vcp)
        
        # Use the location's size and storage code
        pallet_size = loc["Size"]
        storage_code = loc["StorageCode"]  # <-- now matches the location

        aisle, bin_num, level = loc["Aisle"], loc["Bin"], loc["Level"]
        status = "STORED"

        cur.execute("""
            INSERT INTO pallet(
                PalletID, Dept, Class, Item, Quantity, VCP, SSP, Size, StorageCode, 
                Aisle, Bin, Level, Status, CreateDate, CreateID, PutDate, PutID
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            pallet_id, dept, cls, item_code, qty, vcp, ssp, pallet_size, storage_code,
            aisle, bin_num, level,
            status,
            ISO_NOW, created_by,
            ISO_NOW, created_by
        ))

        # Update location to occupied
        cur.execute("""
            UPDATE locations 
            SET Status='OCCUPIED' 
            WHERE Aisle=? AND Bin=? AND Level=?
        """, (aisle, bin_num, level))

        filled += 1

    db.commit()
    messagebox.showinfo("Done", f"✅ Populated {filled} pallets into locations (~{fill_percent*100}%).")

def populate_users():
    """Populate the users table with default users."""
    try:
        db = sqlite3.connect(db_path)
        cur = db.cursor()

        users = [
            (1, "admin", "password123", "Admin", "All"),      # Admin user
            (2, "worker1", "123", "Worker", "General"),       # Example worker
            (3, "im1", "123", "Inventory Manager", "All"),    # Inventory manager
            (4, "om1", "123", "Operations Manager", "All")    # Operations manager
        ]

        # Insert users, ignoring duplicates if they already exist
        for user in users:
            cur.execute("""
                INSERT OR IGNORE INTO users (UserID, UserName, Password, Role, Department)
                VALUES (?, ?, ?, ?, ?)
            """, user)

        db.commit()
        messagebox.showinfo("Success", "Default users created successfully!")

    except Exception as e:
        messagebox.showerror("Error", f"Could not populate users:\n{e}")

def populate_labels():
    """Placeholder function for populating the labels table."""
    messagebox.showinfo("Coming Soon", "Label generation is not implemented yet.")

def generateRandomData(selected_checkboxes):
    selected = [name for name, var in selected_checkboxes.items() if var.get()]
    if not selected:
        messagebox.showwarning("No Selection", "Please select at least one table to generate data for.")
        return

    confirm = messagebox.askyesno("Confirm", f"Generate random data for: {', '.join(selected)}?")
    if not confirm:
        return

    try:
        for table in selected:
            if table == "storageCodes":
                populate_storageCodes()
            elif table == "items":
                populate_items()
            elif table == "locations":
                populate_locations()
            elif table == "pallet":
                populate_pallets()
            elif table == "users":
                populate_users()
            elif table == "labels":
                populate_labels()

        db.commit()
    except Exception as e:
        db.rollback()
        messagebox.showerror("Error", f"Failed to generate data:\n{e}")

def export_database_to_excel():
    try:
        db = sqlite3.connect(db_path)
        
        # Get all table names
        cur = db.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cur.fetchall()]

        if not tables:
            messagebox.showwarning("No Tables", "No tables found in the database.")
            return

        # Ask user where to save the Excel file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Database Export As"
        )
        if not file_path:
            return

        # Export each table to a separate sheet
        with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
            for table in tables:
                df = pd.read_sql_query(f"SELECT * FROM {table}", db)
                df.to_excel(writer, sheet_name=table, index=False)

        messagebox.showinfo("Success", f"Database exported successfully to:\n{file_path}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to export database:\n{e}")

    finally:
        db.close()

# ---------- GUI SETUP ----------
root = tk.Tk()
root.title("Warehouse Database Manager")
root.geometry("420x700")

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

# Random Data Section
rand_frame = ttk.LabelFrame(main_frame, text="Generate Random Data For", padding=10)
rand_frame.pack(pady=10, fill="x")

rand_checkboxes = {}
for tbl in tables:
    var = tk.BooleanVar()
    rand_checkboxes[tbl] = var
    ttk.Checkbutton(rand_frame, text=tbl, variable=var).pack(anchor="w", pady=2)

ttk.Button(main_frame, text="Generate Data for Selected Tables",
           command=lambda: generateRandomData(rand_checkboxes)).pack(pady=5, fill="x")

ttk.Button(main_frame, text="Export Database to Excel", command=export_database_to_excel).pack(pady=5, fill="x")

# Quit button (optional)
ttk.Button(main_frame, text="Exit", command=root.destroy).pack(pady=5, fill="x")

root.mainloop()