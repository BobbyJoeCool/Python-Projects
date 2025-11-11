# This module creates the Inventory Manager GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font
import logic.validators as val
import logic.functions as func
import database.getData as getData

class LocationManagerGUI():

# Create the ELA Tab
    def buildELA(self):
# Create Variables for ELA Frame
        message = tk.StringVar()

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
        messageDisplay = ttk.Label(elaFrame, textvariable=message, anchor="center")
        storageLabel.grid(column=0, row=0, pady=(0,10))
        storageEntry.grid(column=1, row=0, pady=(0,10))
        sizeLabel.grid(column=2, row=0, pady=(0,10), padx=(20,0))
        sizeEntry.grid(column=3, row=0, pady=(0,10))
        messageDisplay.grid(column=0, columnspan=4, row=2, pady=10, sticky="nsew")

    # Setup the Treeview when Enter is
        def findAisle(event=None):
            if val.StorageCode(self.storageCode.get()):
                if val.Size(self.size.get()):
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

                else:
                    message.set("Invalid Size!")
            else:
                message.set("Invalid Storage Code!")    
        
        sizeEntry.bind("<Return>", findAisle)
        storageEntry.bind("<Return>", findAisle)
    

# Create the ELZ Tab
    # Setup the Treeview when Enter is hit

    def buildELZ(self):
    # Configure Variables

    # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.elzTab)
        centerWrapper.pack(expand=True, fill="both")
        self.elzFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        self.elzFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create and Configure Widgets for ELZ Tab
        storageLabel = ttk.Label(self.elzFrame, text="Enter Storage Code")
        self.storageEntryELZ = ttk.Entry(self.elzFrame, textvariable=self.storageCode)
        aisleLabel = ttk.Label(self.elzFrame, text="Enter Aisle:")
        self.aisleEntryELZ = ttk.Entry(self.elzFrame, textvariable=self.aisle)
        storageLabel.grid(column=0, row=0, pady=(0,10))
        self.storageEntryELZ.grid(column=1, row=0, pady=(0,10))
        aisleLabel.grid(column=2, row=0, pady=(0,10), padx=(20,0))
        self.aisleEntryELZ.grid(column=3, row=0, pady=(0,10))        
        
    def findAisle(self, event=None):
        # Widget for displaying empty Locations
        emptyLocationsColumns = ("Sizes", "Zone 1", "Zone 2", " Zone 3", "Zone 4")
        emptyLocations = ttk.Treeview(self.elzFrame, columns=emptyLocationsColumns, show="headings")
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
        oddSideColumnsSetup = ttk.Treeview(self.elzFrame, columns=oddSideColumns, show="headings")
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
        evenSideColumnsSetup = ttk.Treeview(self.elzFrame, columns=evenSideColumns, show="headings")
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

        self.aisleEntryELZ.bind("<Return>", self.findAisle)
        self.storageEntryELZ.bind("<Return>", self.findAisle)

        # Fuction for changing to the ELZ tab to autopopulate if info is filled in.
    def changeTabs(self, event):
        selectedTab = event.widget.select()
        tabText = event.widget.tab(selectedTab, "text")

        if tabText == "Empty Location by Zone":
            if val.Aisle(self.aisle.get()) and val.StorageCode(self.storageCode.get()):
                self.findAisle()

# Create the WLI Tab
    def buildWLI(self):
        # Local Variables for WLI
        dept = tk.StringVar()
        cls = tk.StringVar()
        item = tk.StringVar()
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
        displayMessage = tk.StringVar()

        # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.wliTab)
        centerWrapper.pack(expand=True, fill="both")
        wliFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        wliFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

        # Create Widgets for WLI
        entryFrame = ttk.Frame(wliFrame)
        locationLabel = ttk.Label(entryFrame, text="Location:")
        aisleEntry = ttk.Entry(entryFrame, textvariable=aisle, width=3)
        separaterLabel1 = ttk.Label(entryFrame, text="-")
        binEntry = ttk.Entry(entryFrame, textvariable=bin, width=3)
        separaterLabel2 = ttk.Label(entryFrame, text="-")
        levelEntry = ttk.Entry(entryFrame, textvariable=level, width=2)
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
        itemIDFrame = ttk.Frame(wliFrame)
        itemIDLabel = ttk.Label(itemIDFrame, text="DPCI:")
        deptDisplay = ttk.Label(itemIDFrame, textvariable=dept)
        separaterLabel3 = ttk.Label(itemIDFrame, text="-")
        classDisplay = ttk.Label(itemIDFrame, textvariable=cls)        
        separaterLabel4 = ttk.Label(itemIDFrame, text="-")
        itemDisplay = ttk.Label(itemIDFrame, textvariable=item)        
        itemNameLabel = ttk.Label(wliFrame, text="Item Name:")
        itemNameDisplay = ttk.Label(wliFrame, textvariable=itemName)
        cartonCountLabel = ttk.Label(wliFrame, text="Carton Count:")
        cartonCountDisplay = ttk.Label(wliFrame, textvariable=cartonCount)
        displayMessageDisplay = ttk.Label(wliFrame, textvariable=displayMessage, font=self.bold_font)
        
        # Grid Widgets for WLI
        entryFrame.grid(column=0, columnspan=4, row=0, pady=10)
        locationLabel.pack(side="left")
        aisleEntry.pack(side="left")
        separaterLabel1.pack(side="left")
        binEntry.pack(side="left")
        separaterLabel2.pack(side="left")
        levelEntry.pack(side="left")
        pidLabel.grid(column=4, row=0, pady=10, padx=(10,0))
        pidDisplay.grid(column=5, row=0, pady=10)
        storageLabel.grid(column=0, row=1, pady=10, padx=(10,0))
        storageDisplay.grid(column=1, row=1, pady=10)
        sizeLabel.grid(column=2, row=1, pady=10, padx=(10,0))
        sizeDisplay.grid(column=3, row=1, pady=10)
        zoneLabel.grid(column=4, row=1, pady=10, padx=(10,0))
        zoneDisplay.grid(column=5, row=1, pady=10)
        cartonCountLabel.grid(column=0, row=2, pady=10)
        cartonCountDisplay.grid(column=1, row=2, pady=10)
        itemIDFrame.grid(column=2, columnspan=4, row=2, pady=10, padx=(10,0))
        itemIDLabel.pack(side="left")
        deptDisplay.pack(side="left")
        separaterLabel3.pack(side="left")
        classDisplay.pack(side="left")
        separaterLabel4.pack(side="left")
        itemDisplay.pack(side="left")
        itemNameLabel.grid(column=0, columnspan=2, row=3, pady=10)
        itemNameDisplay.grid(column=2, columnspan=4, row=3, pady=10)
        locationStatusLabel.grid(column=0, row=4, pady=10)
        locationStatusDisplay.grid(column=1, row=4, pady=10)
        displayMessageDisplay.grid(column=2, columnspan=4, row=4, pady=10, padx=(20,0))
        
        # WLI Functions
        def findLocation(self, aisle, bin, level, event=None):
            location = aisle + bin + level
            if val.LocationExists(location):
                locationInfo = getData.GetLocationInfo(location)
                palletInfo = getData.LocGetPallet(location)
                status.set(locationInfo["Status"])
                size.set(locationInfo["Size"])
                zone.set(locationInfo["Zone"])
                storageCode.set(locationInfo["StorageCode"])     
                if palletInfo:
                    name = getData.DPCIgetName(palletInfo["Dept"], palletInfo["Class"], palletInfo["Item"])
                    dept.set(palletInfo["Dept"])
                    cls.set(palletInfo["Class"])
                    item.set(palletInfo["Item"])
                    status.set(palletInfo["Status"])
                    PID.set(palletInfo["PalletID"])
                    itemName.set(name)
                    cartonCount.set(palletInfo["Quantity"])
                else:
                    dept.set("")
                    cls.set("")
                    item.set("")
                    PID.set("")
                    itemName.set("")
                    cartonCount.set("")
                    displayMessage.set("")
            else:
                displayMessage.set("Invalid Location")

        aisleEntry.bind("<Return>", lambda event: findLocation(self, aisle.get(), bin.get(), level.get(), event))
        binEntry.bind("<Return>", lambda event: findLocation(self, aisle.get(), bin.get(), level.get(), event))
        levelEntry.bind("<Return>", lambda event: findLocation(self, aisle.get(), bin.get(), level.get(), event))
        func.LimitRefocus(aisle, binEntry, 3)
        func.LimitRefocus(bin, levelEntry, 3)
        func.LimitRefocus(level, aisleEntry, 2)
                

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
        self.notebook.add(self.elzTab, text="Empty Location by Zone")
        self.notebook.add(self.wliTab, text="Warehouse Location Inquiry")
        self.notebook.add(self.isiTab, text="Item Storage Inquiry")

        self.notebook.bind("<<NotebookTabChanged>>", self.changeTabs)

        self.buildELA()
        self.buildELZ()
        self.buildWLI()