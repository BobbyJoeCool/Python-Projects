# This module creates the Inventory Manager GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font

class OperationsManagerGUI():

# Create the LSU Tab

# Create the CUI Tab

# Create the CHL Tab

# Initialization
    def __init__(self, root, notebookFrame):
        root.title("Operations Manager Functions")

        self.style = ttk.Style()
        self.bold_font = font.Font(family="Arial", size=16, weight="bold")

        # Create the Notebook for the tab system
        self.notebook = ttk.Notebook(notebookFrame)
        self.notebook.pack(fill='both', expand=True)

        self.lsuTab = ttk.Frame(notebookFrame)
        self.cuiTab = ttk.Frame(notebookFrame)
        self.chlTab = ttk.Frame(notebookFrame)

        self.notebook.add(self.lsuTab, text="Location Setup")
        self.notebook.add(self.cuiTab, text="Create User ID")
        self.notebook.add(self.chlTab, text="Clear Hung Location")