# This module creates the Warehouse Worker GUI functions.

import tkinter as tk
from tkinter import messagebox, ttk, font
import logic.validators as val
import logic.functions as func

class WarehouseWorkerGUI():
# Create the PIP Tab
    def buildPIP(self):
    # Build PIP Variables
        pullMode = tk.StringVar()
        labelID = tk.StringVar()
        palletQuantity = tk.IntVar()
        pullQuantity = tk.IntVar()
        palletLoc = tk.StringVar()
        palletItemID = tk.StringVar()
        palletItemName = tk.StringVar()
        palletID = tk.StringVar()
        palletStatus = tk.StringVar()
        altID = tk.StringVar()
        pullStatus = tk.StringVar()

    # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.pipTab)
        centerWrapper.pack(expand=True, fill="both")
        pipFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        pipFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create all the Widgets for the Tab
        pullModeLabel = ttk.Label(pipFrame, text="Pull Mode:")
        pullModeEntry = ttk.Entry(pipFrame, textvariable=pullMode,width=2)
        labelIDLabel = ttk.Label(pipFrame, text="Scan Label:")   
        labelIDEntry = ttk.Entry(pipFrame, textvariable=labelID, width=15)
        palletLocLabel = ttk.Label(pipFrame, text="Location:", font=self.bold_font)
        palletLocDisplay = ttk.Label(pipFrame, textvariable=palletLoc, width=10, font=self.bold_font)
        palletItemIDLabel = ttk.Label(pipFrame, text="DPCI:")
        palletItemIDDisplay = ttk.Label(pipFrame, textvariable=palletItemID, width=11)
        palletItemNameLabel = ttk.Label(pipFrame, text="Item Name:")
        palletItemNameDisplay = ttk.Label(pipFrame, textvariable=palletItemName)
        palletStatusLabel = ttk.Label(pipFrame, text="Pallet Status:")
        palletStatusDisplay = ttk.Label(pipFrame, textvariable=palletStatus, width=20)
        palletIDLabel = ttk.Label(pipFrame, text="Scan Pallet ID:")
        palletIDEntry = ttk.Entry(pipFrame, textvariable=palletID, width=8)
        palletQuantityLabel = ttk.Label(pipFrame, text="Carton Count:")
        palletQuantityDisplay = ttk.Label(pipFrame, textvariable=palletQuantity, width=3)
        altIDLabel = ttk.Label(pipFrame, text="Scan Alternate ID:")
        altIDEntry = ttk.Entry(pipFrame, textvariable=altID, width=8)
        pullQuantityLabel = ttk.Label(pipFrame, text="Pull Quantity:")
        pullQuantityDisplay = ttk.Label(pipFrame, textvariable=pullQuantity, width=3)
        pullStatusLabel = ttk.Label(pipFrame, textvariable=pullStatus, anchor="center", font=self.bold_font)
    # Grid all the Widgets for the Tab
        pullModeLabel.grid(column=0, row=0, pady=10, sticky="e")
        pullModeEntry.grid(column=1, row=0, padx=(0, 20), pady=10, sticky="w")
        labelIDLabel.grid(column=2, row=0, pady=10, sticky="e")
        labelIDEntry.grid(column=3, row=0, columnspan=3, pady=10, sticky="w")
        palletLocLabel.grid(column=0, row=1, pady=10, sticky="e")
        palletLocDisplay.grid(column=1, row=1, padx=(0, 10), pady=10, sticky="w")
        palletItemIDLabel.grid(column=2, row=1, pady=10, sticky="e")
        palletItemIDDisplay.grid(column=3, row=1, pady=10, sticky="w")
        palletStatusLabel.grid(column=4, row=1, pady=10, sticky="e")
        palletStatusDisplay.grid(column=5, row=1, pady=10, sticky="w")
        palletItemNameLabel.grid(column=0, row=2, pady=10, sticky="e")
        palletItemNameDisplay.grid(column=1, columnspan=5, row=2, pady=10, sticky="w")
        palletIDLabel.grid(column=0, row=3, pady=(10,0), sticky="e")
        palletIDEntry.grid(column=1, columnspan=3, row=3, pady=(10,0), sticky="w")
        palletQuantityLabel.grid(column=4, row=3, pady=(10,0), sticky="e")
        palletQuantityDisplay.grid(column=5, row=3, pady=(10,0), sticky="w")
        altIDLabel.grid(column=0, row=4, pady=(0,10), sticky="e")
        altIDEntry.grid(column=1, columnspan=2, row=4, pady=(0,10), sticky="w")
        pullQuantityLabel.grid(column=4, row=4, pady=(0,10), sticky="e")
        pullQuantityDisplay.grid(column=5, row=4, pady=(0,10), sticky="w")
        pullStatusLabel.grid(column=0, columnspan=6, row=5, pady=10, sticky="nsew")

        def pip_scan_label_ID(event=None):
            label = labelID.get()
            pullCode = pullMode.get()
            validate = val.PullCode(pullCode)
            if validate:
                validate = val.LabelID(label)
                if not validate:
                    pullStatus.set("Error!  Invalid Label!")
                else:
                    palletLoc.set("300-001-01")
                    palletItemID.set("100-10-1000")
                    palletItemName.set("Huggies Diapers Size 4 - 60 CT")
                    palletStatus.set("Pull Pending")
                    pullStatus.set("Scan Pallet ID or   Alternate ID")
                    palletQuantity.set(50)
                    pullQuantity.set(10)
                    palletIDEntry.focus_set()
            else:
                pullStatus.set("Error! Invalid Pull Code!")

        def pip_scan_pallet_ID(event=None):
            if not val.PID(palletID.get()):
                pullStatus.set("Error!  Invalid Pallet ID!")
            else:
                palletQuantity.set(40)
                palletStatus.set("Stored")
                pullStatus.set("Pull Successful!")
                pullQuantity.set(0)
                labelID.set("")
                palletID.set("")
                altID.set("")
                labelIDEntry.focus_set()
        
        def pip_scan_alt_ID(event=None):
            loc = altID.get()
            splitlocation = func.splitLocation(loc)
            if splitlocation:
                aisle1, bin1, level1 = splitlocation
                if val.LocationExists(aisle1, bin1, level1):
                    if altID.get() == palletLoc.get().replace("-",""):
                        palletQuantity.set(40)
                        palletStatus.set("Stored")
                        pullStatus.set("Pull Successful!")
                        pullQuantity.set(0)
                        labelID.set("")
                        palletID.set("")
                        altID.set("")
                        labelIDEntry.focus_set()
                    else:
                        pullStatus.set("Error!  Wrong Location!")
                else:
                    pullStatus.set("Error!  Invalid Location!")         
            else:
                pullStatus.set("Error!  Invalid Location!")          

        labelIDEntry.bind("<Return>", pip_scan_label_ID)
        palletIDEntry.bind("<Return>", pip_scan_pallet_ID)
        altIDEntry.bind("<Return>", pip_scan_alt_ID)

# Create the SDP Tab
    def buildSDP(self):
    # Build SDP Variable
        aisle = tk.StringVar()
        storageCode = tk.StringVar()
        palletID = tk.StringVar()
        palletSize = tk.StringVar()
        assignedLoc = tk.StringVar()
        locationID = tk.StringVar()
        palletLoc = tk.StringVar()
        palletStatus = tk.StringVar()
        aisleZone = tk.StringVar()
        palletItemID = tk.StringVar()
        palletItemName = tk.StringVar()
        palletItemQuantity = tk.IntVar()
        displayMessage = tk.StringVar()
        putInProgress = tk.BooleanVar()
        
        def cancelPut(event=None):
            if putInProgress.get():
                assignedLoc.set("")
                putInProgress.set(False)
                displayMessage.set("Put Canceled!")
            else:
                displayMessage.set("Error, no put selected")
            

        def assignLocation(event=None):
            # This function will check the overrides
            # Then set the pallet Size and Storage Code to the pallet ID.
            # It will also look for a location in the override zone FIRST, then start at zone 1.
            if not putInProgress.get():
                if val.PID(palletID.get()):
                    if val.Aisle(aisle.get()):
                        palletItemID.set("100-10-1000")
                        palletItemQuantity.set(90)
                        palletItemName.set("Huggies Diapers Size 4 - 60 CT")
                        assignedLoc.set("300-001-01")
                        palletStatus.set("Put Pending")
                        palletLoc.set("")
                        displayMessage.set("Awating Put Confirmation")
                        putInProgress.set(True)
                        locationIDEntry.focus_set()
                    else:
                        displayMessage.set("Invalid Aisle")
                else:
                    displayMessage.set("Invalid Pallet ID")
            else:
                displayMessage.set("Put in Progress, complete put.")

        def completePut(event=None):
            # This will assign the PID to the assigned location.
            if putInProgress.get():
                if locationID.get() == assignedLoc.get().replace("-", ""):
                    locationID.set("")
                    palletStatus.set("Stored")
                    palletLoc.set("300-001-01")
                    assignedLoc.set("")
                    displayMessage.set("Put Successful!")
                    putInProgress.set(False)
                    palletIDEntry.focus_set()
                else:
                    displayMessage.set("Wrong Location!")
            else:
                displayMessage.set("No Put Selected!")

    # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.sdpTab)
        centerWrapper.pack(expand=True, fill="both")
        sdpFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        sdpFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create Widgets for the SDP Tab
        putAisleLabel = ttk.Label(sdpFrame, text="Aisle:")
        putAisleEntry = ttk.Entry(sdpFrame, textvar=aisle, width=3)
        putZoneLabel = ttk.Label(sdpFrame, text="Override Put Zone:")
        putZoneEntry = ttk.Entry(sdpFrame, textvariable=aisleZone, width=2)
        putSizeLabel = ttk.Label(sdpFrame, text="Override Pallet Size")
        putSizeEntry = ttk.Entry(sdpFrame, textvariable=palletSize, width=2)
        putStorageLabel = ttk.Label(sdpFrame, text="Override Pallet Storage Type:")
        putStorageEntry = ttk.Entry(sdpFrame, textvariable=storageCode, width=2)
        palletIDLabel = ttk.Label(sdpFrame, text="Scan Pallet ID", font=self.bold_font)
        palletIDEntry = ttk.Entry(sdpFrame, textvariable=palletID, width=8, font=self.bold_font)
        assignedLocationLabel = ttk.Label(sdpFrame, text="Assigned Location:", font=self.bold_font)
        assignedLocationDisplay = ttk.Label(sdpFrame, textvariable=assignedLoc, font=self.bold_font)
        palletItemIDLabel = ttk.Label(sdpFrame, text="DPCI:")
        palletItemIDDisplay = ttk.Label(sdpFrame, textvariable=palletItemID)
        palletItemQuantityLabel = ttk.Label(sdpFrame, text="Carton Count:")
        palletItemQuantityDisplay = ttk.Label(sdpFrame, textvariable=palletItemQuantity, width=3)
        palletItemNameLabel = ttk.Label(sdpFrame, text="Item Name:")
        palletItemNameDisplay = ttk.Label(sdpFrame, textvariable=palletItemName)
        locationIDLabel = ttk.Label(sdpFrame, text="Scan Location:")
        locationIDEntry = ttk.Entry(sdpFrame, textvariable=locationID)
        palletStatusLabel = ttk.Label(sdpFrame, text="Pallet Status:")
        palletStatusDisplay = ttk.Label(sdpFrame, textvariable=palletStatus)
        palletLocationLabel = ttk.Label(sdpFrame, text="Stored in:")
        palletLocationDisplay = ttk.Label(sdpFrame, textvariable=palletLoc)
        displayMessageLabel = ttk.Label(sdpFrame, textvariable=displayMessage, anchor="center", font=self.bold_font)
        cancelPutButton = ttk.Button(sdpFrame, text="Cancel Put", command=cancelPut)

    # Put Widgets in the Grid
        putAisleLabel.grid(column=2, row=0, pady=10, sticky="e")
        putAisleEntry.grid(column=3, row=0, pady=10, sticky="w")
        putZoneLabel.grid(column=0, row=1, pady=10, sticky="e")
        putZoneEntry.grid(column=1, row=1, pady=10, sticky="w")
        putSizeLabel.grid(column=2, row=1, pady=10, padx=(10,0), sticky="e")
        putSizeEntry.grid(column=3, row=1, pady=10, sticky="w")
        putStorageLabel.grid(column=4, row=1, pady=10, padx=(10,0), sticky="e")
        putStorageEntry.grid(column=5, row=1, pady=10, sticky="w")
        palletIDLabel.grid(column=1, row=2, pady=10, sticky="e")
        palletIDEntry.grid(column=2, row=2, columnspan=2, pady=10, sticky="w")
        assignedLocationLabel.grid(column=3, row=2, pady=10, padx=(10,0), sticky="e")
        assignedLocationDisplay.grid(column=4, row=2, pady=10, sticky="w")   
        palletItemIDLabel.grid(column=1, row=3, pady=10, sticky="e")
        palletItemIDDisplay.grid(column=2, row=3, pady=10, sticky="w")
        palletItemQuantityLabel.grid(column=3, row=3, pady=10, padx=(10,0), sticky="e")
        palletItemQuantityDisplay.grid(column=4, row=3, pady=10, sticky="w")        
        palletItemNameLabel.grid(column=0, row=4, pady=10, sticky="e")
        palletItemNameDisplay.grid(column=1, row=4, columnspan=5, pady=10, sticky="w")             
        locationIDLabel.grid(column=2, row=5, pady=10, sticky="e")
        locationIDEntry.grid(column=3, row=5, pady=10, sticky="w")
        palletStatusLabel.grid(column=0, row=6, pady=10, sticky="e")
        palletStatusDisplay.grid(column=1, row=6, pady=10, sticky="w")
        palletLocationLabel.grid(column=2, row=6, pady=10, padx=(10,0), sticky="e")
        palletLocationDisplay.grid(column=3, row=6, pady=10, sticky="w")
        cancelPutButton.grid(column=4, columnspan=2, row=6, pady=10, padx=(10,0))
        displayMessageLabel.grid(column=0, columnspan=7, row=7, pady=10, sticky="ew")

        func.LimitRefocus(aisle, palletIDEntry, 3)
        func.BindNextFocus(putAisleEntry, palletIDEntry)

        palletIDEntry.bind("<Return>", assignLocation)
        locationIDEntry.bind("<Return>", completePut)

# Create the MDP Tab
    def buildMDP(self):
        # Build MDP Variable
        palletID = tk.StringVar()
        palletSize = tk.StringVar()
        palletStorageCode = tk.StringVar()
        palletLoc = tk.StringVar()
        palletStatus = tk.StringVar()
        palletItemID = tk.StringVar()
        palletItemName = tk.StringVar()
        palletItemQuantity = tk.IntVar()
        locationID = tk.StringVar()
        displayMessage = tk.StringVar()

        def selectPallet(event=None):
            # This function will check the overrides
            # Then set the pallet Size and Storage Code to the pallet ID.
            # It will also look for a location in the override zone FIRST, then start at zone 1.
            if val.PID(palletID.get()):
                palletItemID.set("100-10-1000")
                palletItemQuantity.set(90)
                palletItemName.set("Huggies Diapers Size 4 - 60 CT")
                palletStatus.set("STORED")
                palletLoc.set("300-001-01")
                displayMessage.set("Pallet Selected")
                palletStorageCode.set("CR")
                palletSize.set("L")
            else:
                displayMessage.set("Invalid Pallet ID!")
            

        def completePut(event=None):
            # This will assign the PID to the assigned location.
            loc = locationID.get()
            splitlocation = func.splitLocation(loc)
            if splitlocation:
                aisle1, bin1, level1 = splitlocation
            else:
                displayMessage.set("Invalid Location!")
                return
            
            oldLoc = palletLoc.get()
            locFormat = f"{loc[:3]}-{loc[3:6]}-{loc[6:]}"
            if val.LocationExists(aisle1, bin1, level1):
                if locFormat != oldLoc:
                    locationID.set("")
                    palletLoc.set(locFormat)
                    palletStatus.set("Stored")
                    displayMessage.set(f"Pallet Moved from {oldLoc}")
                else:
                    displayMessage.set(f"Pallet already stored in {oldLoc}")
            else:
                displayMessage.set("Invalid Location!")

    # Configure the Frame so it is centered in the tab
        centerWrapper = ttk.Frame(self.mdpTab)
        centerWrapper.pack(expand=True, fill="both")
        mdpFrame = ttk.Frame(centerWrapper, padding=10, relief="ridge", borderwidth=2)
        mdpFrame.grid(row=0, column=0)
        centerWrapper.columnconfigure(0, weight=1)
        centerWrapper.rowconfigure(0, weight=1)

    # Create Widgets for the MDP Tab
        palletIDLabel = ttk.Label(mdpFrame, text="Scan Pallet ID", font=self.bold_font)
        palletIDEntry = ttk.Entry(mdpFrame, textvariable=palletID, width=8, font=self.bold_font)
        palletItemIDLabel = ttk.Label(mdpFrame, text="DPCI:")
        palletItemIDDisplay = ttk.Label(mdpFrame, textvariable=palletItemID)
        palletItemQuantityLabel = ttk.Label(mdpFrame, text="Carton Count:")
        palletItemQuantityDisplay = ttk.Label(mdpFrame, textvariable=palletItemQuantity, width=3)
        palletItemNameLabel = ttk.Label(mdpFrame, text="Item Name:")
        palletItemNameDisplay = ttk.Label(mdpFrame, textvariable=palletItemName)
        palletSizeLabel = ttk.Label(mdpFrame, text="Pallet Size:")
        palletSizeDisplay = ttk.Label(mdpFrame, textvariable=palletSize)
        palletStorageCodeLabel = ttk.Label(mdpFrame, text="Storage Code:")
        palletStorageCodeDisplay = ttk.Label(mdpFrame, textvariable=palletStorageCode)
        locationIDLabel = ttk.Label(mdpFrame, text="Scan Location:")
        locationIDEntry = ttk.Entry(mdpFrame, textvariable=locationID)
        palletStatusLabel = ttk.Label(mdpFrame, text="Pallet Status:")
        palletStatusDisplay = ttk.Label(mdpFrame, textvariable=palletStatus)
        palletLocationLabel = ttk.Label(mdpFrame, text="Stored in:")
        palletLocationDisplay = ttk.Label(mdpFrame, textvariable=palletLoc)
        displayMessageLabel = ttk.Label(mdpFrame, textvariable=displayMessage, anchor="center", font=self.bold_font)

    # Put Widgets in the Grid
        palletIDLabel.grid(column=2, row=0, pady=10, sticky="e")
        palletIDEntry.grid(column=3, row=0, columnspan=2, pady=10, sticky="w")    
        palletItemIDLabel.grid(column=0, row=1, pady=10, sticky="e")
        palletItemIDDisplay.grid(column=1, row=1, pady=10, sticky="w")
        palletItemQuantityLabel.grid(column=2, row=1, pady=10, padx=(10,0), sticky="e")
        palletItemQuantityDisplay.grid(column=3, row=1, pady=10, sticky="w")
        palletStorageCodeLabel.grid(column=4, row=1, pady=10, padx=(10,0), sticky="e")
        palletStorageCodeDisplay.grid(column=5, row=1, pady=10, sticky="w")
        palletItemNameLabel.grid(column=0, row=2, pady=10, sticky="e")
        palletItemNameDisplay.grid(column=1, row=2, columnspan=5, pady=10, sticky="w")
        palletStatusLabel.grid(column=0, row=3, pady=10, sticky="e")
        palletStatusDisplay.grid(column=1, row=3, pady=10, sticky="w")
        palletLocationLabel.grid(column=2, row=3, pady=10, padx=(10,0), sticky="e")
        palletLocationDisplay.grid(column=3, row=3, pady=10, sticky="w")
        palletSizeLabel.grid(column=4, row=3, pady=10, padx=(10,0), sticky="e")
        palletSizeDisplay.grid(column=5, row=3, pady=10, sticky="w")
        locationIDLabel.grid(column=2, row=4, pady=10, sticky="e")
        locationIDEntry.grid(column=3, row=4, pady=10, sticky="w")
        displayMessageLabel.grid(column=0, row=5, columnspan=7, sticky="ew")

        palletIDEntry.bind("<Return>", selectPallet)
        locationIDEntry.bind("<Return>", completePut)


#Initialization Function
    def __init__(self, root, notebookFrame):
        root.title("Warehouse Worker Functions")

        self.style = ttk.Style()
        self.bold_font = font.Font(family="Arial", size=16, weight="bold")

        # Create the Notebook for the tab system
        self.notebook = ttk.Notebook(notebookFrame)
        self.notebook.pack(fill='both', expand=True)

        self.pipTab = ttk.Frame(notebookFrame)
        self.sdpTab = ttk.Frame(notebookFrame)
        self.mdpTab = ttk.Frame(notebookFrame)

        self.notebook.add(self.pipTab, text="Pallet ID Pull")
        self.notebook.add(self.sdpTab, text="System Directed Put")
        self.notebook.add(self.mdpTab, text="Manually Directed Put")
        
        self.buildPIP()
        self.buildSDP()
        self.buildMDP()