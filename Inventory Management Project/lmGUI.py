# This module creates the Inventory Manager GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font

class LocationManagerGUI():

# Create the ELA Tab

# Create the ELZ Tab

# Create the WLI Tab

# Create the ISI Tab

# Initialization
    def __init__(self, root, notebookFrame):
        root.title("Location Managment Functions")

        self.style = ttk.Style()
        self.bold_font = font.Font(family="Arial", size=16, weight="bold")

        # Create the Notebook for the tab system
        self.notebook = ttk.Notebook(notebookFrame)
        self.notebook.pack(fill='both', expand=True)

        self.elaTab = ttk.Frame(notebookFrame)
        self.elzTab = ttk.Frame(notebookFrame)
        self.wliTab = ttk.Frame(notebookFrame)
        self.isiTab = ttk.Frame(notebookFrame)

        self.notebook.add(self.elaTab, text="Empty Location by Aisle")
        self.notebook.add(self.elzTab, text="Empty Locatino by Zone")
        self.notebook.add(self.wliTab, text="Warehouse Location Inquiry")
        self.notebook.add(self.isiTab, text="Item Storage Inquiry")