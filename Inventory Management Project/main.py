# This is the Main Program, it contains the main GUI, the login, and some other logics.

import tkinter as tk
from tkinter import ttk, messagebox
from GUI.baseGUI import BaseGUI


def main():
    # Load configuration
    # config = load_config("config/settings.json")

    # Initialize database
    # db = DatabaseManager(config["DATABASE_PATH"])

    # Initialize GUI root
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("1100x900+400+50")
    root.resizable(width=False, height=False)   

    # Pass dependencies into GUI
    app = BaseGUI(root)

    # Start main loop
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Exiting cleanly...")
    finally:
        # Cleanup resources
        # db.close()
        # ys.exit(0)
        print("Database closed.  System Exited.")


if __name__ == "__main__":
    main()