# This module creates the Inventory Manager GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font

class LocationManagerGUI():

# Create the ELA Tab
    def buildELA(self):
# Create Variables for ELA Frame

# Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.elaTab)
        centerWrapper.pack(expand=True, fill="both")
        elaFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        elaFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create and Configure all the Widgets for ELA Tab
        storageLabel = ttk.Label(elaFrame, text="Enter Storage Code")
        storageEntry = ttk.Entry(elaFrame, textvariable=self.storageCode)
        sizeLabel = ttk.Label(elaFrame, text="Enter Size:")
        sizeEntry = ttk.Entry(elaFrame, textvariable=self.size)
        storageLabel.grid(column=0, row=0, pady=(0,10))
        storageEntry.grid(column=1, row=0, pady=(0,10))
        sizeLabel.grid(column=2, row=0, pady=(0,10), padx=(20,0))
        sizeEntry.grid(column=3, row=0, pady=(0,10))

    # Setup the Treeview when Enter is
        def findAisle(event=None):
            columns = ("Aisle", "HS", "S", "M", "L")
            displayBox = ttk.Treeview(elaFrame, columns=columns, show="headings")
            displayBox.grid(column=0, columnspan=4, row=1, sticky="nsew")

            for col in columns:
                displayBox.heading(col, text=col)
                displayBox.column(col, width=100, anchor="center")
            
            data = [
                ("300","97","27","",""),
                ("301","","","97",""),
                ("302","","","","57"),
            ]

            for row in data:
                displayBox.insert("","end", values=row)

            def on_row_select(event=None):
                selectedAisle = displayBox.selection()
                if not selectedAisle:
                    return
                item = displayBox.item(selectedAisle[0])
                values = item["values"]
                if values:
                    self.aisle.set(values[0])
            
            displayBox.bind("<<TreeviewSelect>>", on_row_select)

            

        
        sizeEntry.bind("<Return>", findAisle)
        storageEntry.bind("<Return>", findAisle)
    

# Create the ELZ Tab
    def buildELZ(self):
    # Configure Variables

    # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.elzTab)
        centerWrapper.pack(expand=True, fill="both")
        elzFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        elzFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create and Configure Widgets for ELZ Tab
        storageLabel = ttk.Label(elzFrame, text="Enter Storage Code")
        storageEntry = ttk.Entry(elzFrame, textvariable=self.storageCode)
        aisleLabel = ttk.Label(elzFrame, text="Enter Aisle:")
        aisleEntry = ttk.Entry(elzFrame, textvariable=self.aisle)
        storageLabel.grid(column=0, row=0, pady=(0,10))
        storageEntry.grid(column=1, row=0, pady=(0,10))
        aisleLabel.grid(column=2, row=0, pady=(0,10), padx=(20,0))
        aisleEntry.grid(column=3, row=0, pady=(0,10))

    # Setup the Treeview when Enter is hit
        def findAisle(event=None):
            # Widget for displaying empty Locations
            emptyLocationsColumns = ("Sizes", "Zone 1", "Zone 2", " Zone 3", "Zone 4")
            emptyLocations = ttk.Treeview(elzFrame, columns=emptyLocationsColumns, show="headings")
            emptyLocations.grid(column=0, columnspan=4, row=1, sticky="ew")

            for col in emptyLocationsColumns:
                emptyLocations.heading(col, text=col)
                emptyLocations.column(col, width=100, anchor="center")
            
            emptyLocationsData = [
                ("L","0","0","0","0"),
                ("M","0","0","0","0"),
                ("S","13","15","18","21"),
                ("HS","8","9","7","23"),
            ]
            for row in emptyLocationsData:
                emptyLocations.insert("","end", values=row)

        # Widget for displaying Aisle Setup
            oddSideColumns = ("ODD SIDE", "Zone 1", "Zone 2", " Zone 3", "Zone 4")
            oddSideColumnsSetup = ttk.Treeview(elzFrame, columns=oddSideColumns, show="headings")
            oddSideColumnsSetup.grid(column=0, columnspan=4, row=2, sticky="ew")

            for col in oddSideColumns:
                oddSideColumnsSetup.heading(col, text=col)
                oddSideColumnsSetup.column(col, width=100, anchor="center")
            
            oddSideData = [
                ("10","CR-M","CR-M","CR-M","CR-M"),
                ("9","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("8","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("7","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("6","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("5","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("4","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("3","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("2","CR-HS","CR-HS","CR-HS","CR-HS"),
                ("1","TR-M","TR-M","TR-M","TR-M"),
            ]
            for row in oddSideData:
                oddSideColumnsSetup.insert("","end", values=row)

            evenSideColumns = ("EVEN SIDE", "Zone 1", "Zone 2", " Zone 3", "Zone 4")
            evenSideColumnsSetup = ttk.Treeview(elzFrame, columns=evenSideColumns, show="headings")
            evenSideColumnsSetup.grid(column=0, columnspan=4, row=3, sticky="ew")

            for col in evenSideColumns:
                evenSideColumnsSetup.heading(col, text=col)
                evenSideColumnsSetup.column(col, width=100, anchor="center")
            
            evenSideData = [
                ("8","CR-S","CR-S","CR-S","CR-S"),                
                ("7","CR-S","CR-S","CR-S","CR-S"),
                ("6","CR-S","CR-S","CR-S","CR-S"),
                ("5","CR-S","CR-S","CR-S","CR-S"),
                ("4","CR-S","CR-S","CR-S","CR-S"),  
                ("3","CR-S","CR-S","CR-S","CR-S"),                              
                ("2","CR-S","CR-S","CR-S","CR-S"),
                ("1","TR-M","TR-M","TR-M","TR-M"),
            ]
            for row in evenSideData:
                evenSideColumnsSetup.insert("","end", values=row)                
        
        aisleEntry.bind("<Return>", findAisle)
        storageEntry.bind("<Return>", findAisle)




# Create the WLI Tab
    def buildWLI(self):
        # Local Variables for WLI
        dept = tk.StringVar()
        cls = tk.StringVar()
        item = tk.StringVar()
        itemID = tk.StringVar()
        storageCode = tk.StringVar()
        size = tk.StringVar()
        aisle = tk.StringVar()
        bin = tk.StringVar()
        level = tk.StringVar()
        zone = tk.StringVar()
        PID = tk.StringVar()
        status = tk.StringVar()
        itemName = tk.StringVar()
        cartonCount = tk.StringVar()

        # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.wliTab)
        centerWrapper.pack(expand=True, fill="both")
        wliFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        wliFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

        # Create Widgets for WLI
        aisleLabel = ttk.Label(wliFrame, text="Aisle:")
        aisleEntry = ttk.Entry(wliFrame, textvariable=aisle)
        binLabel = ttk.Label(wliFrame, text="Bin:")
        binEntry = ttk.Label(wliFrame, textvariable=bin)
        levelLabel = ttk.Label(wliFrame, text="Level:")
        levelEntry = ttk.Entry(wliFrame, textvariable=level)
        storageLabel = ttk.Label(wliFrame, text="Storage Code:")
        storageDisplay = ttk.Label(wliFrame, textvariable=storageCode)
        sizeLabel = ttk.Label(wliFrame, text="Size:")
        sizeDisplay = ttk.Label(wliFrame, textvariable=size)
        zoneLabel = ttk.Label(wliFrame, text="Zone:")
        zoneDisplay = ttk.Label(wliFrame, textvariable=zone)
        pidLabel = ttk.Label(wliFrame, text="Pallet ID:")
        pidDisplay = ttk.Label(wliFrame, textvariable=PID)
        locationStatusLabel = ttk.Label(wliFrame, text="Location Status")
        locationStatusDisplay = ttk.Label(wliFrame, textvariable=status)
        itemIDLabel = ttk.Label(wliFrame, text="DPCI:")
        itemIDDisplay = ttk.Label(wliFrame, textvariable=itemID)
        itemNameLabel = ttk.Label(wliFrame, text="Item Name:")
        itemNameDisplay = ttk.Label(wliFrame, textvariable=itemName)
        cartonCountLabel = ttk.Label(wliFrame, text="Carton Count:")
        cartonCountDisplay = ttk.Label(wliFrame, textvariable=cartonCount)

        # Grid Widgets for WLI

        # WLI Functions

# Create the ISI Tab

# Initialization
    def __init__(self, root, notebookFrame):
        root.title("Location Managment Functions")
        self.aisle = tk.StringVar()
        self.storageCode = tk.StringVar()
        self.size = tk.StringVar()
        self.PID = tk.StringVar()

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

        self.buildELA()
        self.buildELZ()