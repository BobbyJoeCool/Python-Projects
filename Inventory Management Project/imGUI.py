# This module creates the Inventory Manager GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font

class InventoryManagerGUI():

# Create the IUP Tab

# Create the PII Tab

# Create the PAR Tab

# Initialization
    def __init__(self, root, notebookFrame):
        root.title("Inventory Manager Functions")

        self.style = ttk.Style()
        self.bold_font = font.Font(family="Arial", size=16, weight="bold")

        # Create the Notebook for the tab system
        self.notebook = ttk.Notebook(notebookFrame)
        self.notebook.pack(fill='both', expand=True)

        self.iupTab = ttk.Frame(notebookFrame)
        self.piiTab = ttk.Frame(notebookFrame)
        self.parTab = ttk.Frame(notebookFrame)

        self.notebook.add(self.iupTab, text="Item Lookup")
        self.notebook.add(self.piiTab, text="Pallet ID Inquiry")
        self.notebook.add(self.parTab, text="Pallet Reinstate")