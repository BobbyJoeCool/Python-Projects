# Passion Project/Can I do it Project

This project is more of a "can I do it" project than anything else.  It is an attempt to see if I can recreate the wareshousing functionality of the Inventory Management Systems that we use at work.  There are several parts of the functionality that need to be replicated, and this document will help to keep track of the database tables required, the User Information required, the GUI required (I may write a seperate module for each function of the GUI since each one would be very complex, with a module for all the database retreival functions).

## GUI Functions

### PIP - Pallet ID Pull
Scan a label, then scan a pallet ID to pull a box or pallet from a location.  Automatically reduces the number of boxes by the appropriate amount from that location.

#### Design for GUI
- Entry Box for Pull Mode
    - CA - Carton Air (Pulls single or multiple boxes)
    - FP - Full Pallet (Pulls the remainder of the pallet)
- Entry Box for Label ID: (Meant to be scanned.  Activated on "Enter")
- Display Label for Pallet Location (Populates on Scanning Label ID)
- Display Label for Pallet DPCI (Populates on Scanning Label ID)
- Display Label for Pallet Quantity (Populates on Scanning Label ID)
- Display Label for Pull Quantity (Populates on Scanning Label ID)
- Entry Box for Pallet ID: (Meant to be Scanned: Activated on "Enter")
    - When Activated, confirms the pull is completed.
    - Updates the Pallet Information and Pallet Display with current quantity
- Alternate Entry Box for Location ID: (Meant to be Scanned: Activated on "Enter")
    - Works the same as the Pallet ID box, meant to be used if Pallet ID is missing.

### IUP - Item Lookup
Enter the Item ID (DP-C-I), and it brings up all the information about the item

#### GUI Design

- Entry Box for Department
- Entry Box for Class
- Entry Box for Item
    - These activate when Enter is pressed in any box, and populate the following display boxes.
- Display Label for Item Name
- Display Label for Item Description (Longer)
- Display Label for Item default Storage Code
- Display Label for Item Retail Price
- Display Label for Item Wholesale Cost.
- Display Label for VCP/SSP (Vendor Case Pack/Store Ship Pack, currently unused, VCP/SSP should be the same for all items)

### ISI - Item Storage Informaion
Enter the Item ID and it brings up a list of every location where the item is in the warehouse

#### GUI Design
- Entry Box for Department
- Entry Box for Class
- Entry Box for Item
  - These activate when Enter is pressed in any box, and populate the following display boxes.
- A Table of Locations with pallet IDs that currently hold this product with this following informaiton:
    - LocationID, Pallet ID, Quantity, Storage Status
- A button that will take you to the PII screen for the selected pallet.

### PII - Pallet ID Information
Enter the Pallet ID, and bring up all information about that pallet.

#### GUI Design
- Entry Box for Pallet ID
    - When "enter" is hit on this box, populate the rest of the screen.
- Label for Department
- Label for Class
- Label for Item
- Label for Aisle
- Label for Bin
- Label for Level
- Label for Quantity
- Label for VCP/SSP (Currently Unused, but will have the Vendor Case Pack)
- Label for Storage Code
- Label for Pallet Size
- Label for Pallet Status
- Label for Product Expiration Date (if Applicable)
- Label for Pallet Create Date
- Label for Pallet Create User ID
- Label for Pallet Put Date
- Label for Pallet Put User ID
- Label for Pallet Pull Date (lists last time pulled from)
- Label for Pallet Pull User ID

### SDP - System Directed Put
Enter the aisle you are in, and the system finds the first open location that matches the storage code and size of the pallet ID you scan.  When you scan or enter the location, it systematically puts the pallet ID in that location.

#### GUI Design
- Entry Box for Aisle
- Entry Box for Pallet Size (Overrides Pallet Size, Defaults to PID if left blank)
- Entry Box for Storage Code (Overrides Pallet Storage Code, Defaults to PID if left blank)
- Entry Box for Pallet ID
    - Activates on hitting return, searches for an empty location matching the pallets storage code and size in the aisle selected.
    - Should Check Pallet Status and only allow the move/put of pallets that are "STORED" or "ACTIVE."  If they are "PENDING," "PULLED," "CANCELED," or any others, an error should pop up.
- Label for directed Location (return "No Location Found, of None")
- Entry Box for the Location ID
    - Upon Entering the Location (ignore the level entered), ask user to verify the level with a popup box.
    - Once the put is confirmed, display "Pallet Put" or "Pallet moved from {previous location}"

### MDP - Manualy Directed Put
Allows the user to manually force a pallet into a location, even if another pallet ID is already in that location.  If there is another pallet in location, a warning should pop up stating this and asking if they want to proceed.  If the pallets have the same item code, combine the two pallets (add the quantities together).  If the pallets have different item codes, store BOTH pallet IDs in this location.

#### GUI Design

- Entry Box for Pallet ID
    - Should Check Pallet Status and only allow the move/put of pallets that are "STORED" or "ACTIVE."  If they are "PENDING," "PULLED," "CANCELED," or any others, an error should pop up.
- Entry Box for new Location
    - Pop up asking the user to verify the level put to.
    - Upon entering the new location, program should check to see if the location is empty.  If it is, put the pallet there.  The pallet will adopt the storage code and size of the location it is moved to.
    - The the pallets have the same DPCI, combine the pallets under the Pallet ID that is currently in the location.  
        - If products have an expiration date, pop up a verification box and tell the user that the closest date will be chosen for all product at the location.
    - If the location is occupied, pop up a message telling the user that the location is systematically occupied.  Ask them if they would like to continue anyway.
    - Once the put is confirmed, display "Pallet Put" or "Pallet moved from {previous location}"


## Inventory Manager Functions

### PII - Pallet ID Information - Addendum
Extra functionality that IMs have that they can edit the pallet information on this screen

#### GUI Interface added functionality
Adds a function to this screen where, when selected, brings up a new window with an editing GUI.

All Entry Boxes should automatically populat with the current information, but be editable.

- Dropdown: Reason Code (Enter a code for the reason for the change)
    - 1: Overage
    - 2: Shortage
    - 3: Incorrect VCP/SSP
    - 4: Incorrect DPCI
    - 5: Incorrect Expiration Date
    - 6: Damage
- Entry Boxes: Department, Class, Item 
    - Upon entry, a Verification that this is a valid DPCI should occur
- Entry Box: Quantity 
- Entry Box: VCP/SSP 
- Entry Box: Expiration Date
- Confirm Button

### IUP - Item Lookup - Addendum
Extra functionality that IMs have that they can edit the item information on this screen (Description, Storage Code)

#### GUI Design

Similar to the PII interface, a button should bring up a popup that allows the editing of the item.  All fields should automatically populate with current information, but allow editing.

- Department (Should be locked with a checkbox to make it harder to edit)
- Class (Should be locked with a checkbox to make it harder to edit)
- Item (Should be locked with a checkbox to make it harder to edit)
    - Upon changing any of these three, it should automatically verify that this DPCI isn't already in use by another product.
- Item Name
- Item Description
- Item Retail Price
- Item Wholesale Cost
- Expected VCP/SSP
- Default Storage Code
- Expiration Date Required
- Confirm Button

### PAR - Pallet Reinstate
Create a Pallet - Enter Item ID, Quantity, Size, and optionally a location, and creates a pallet (with a unique Pallet ID and a storage code that matches the Item ID)

#### GUI Design
All 
- Department
- Class
- Item
    - Verify that this DPCI is valid.  These cannot be blank.
- Aisle
- Bin
- Level
    - These can be left blank, if they are, Pallet Status will be PENDING PUT.
    - If a location is selected, verify the location is empty.  Pallets cannot be reinstated to an occupied locatin.
- Quantity
    - Cannot be blank.
- VCP/SSP (Currently Unused, but will have the Vendor Case Pack)
    - If left blank, use the default for the item.
- Storage Code
    - If left blank, us the item default
- Pallet Size
    - Cannot be blank
- Label for Product Expiration Date
    - If left blank, check DPCI if it requires an expiration date.  Flag with error if it does.
- Create Pallet Button
    - Display Pallet ID (Also, print to Terminal)

## Operations Manager GUI Functions

### LSU - Location Setup
Allows the setup of locations.  Sets locations by aisle, starting at a certain bin and level, and ending at another bin and level (for example, creating aisle 310, bin 1-128, levels 2-10, all Storage Code CR, Size HS.). ALso allows the editing of locations already set up.

- Aisle Entry Box:
- Aisle Setup:
    - Entry: Number of Bins
    - Entry: Number of Zones
    - Label: Each Zones Final Bin
    - Confirm Button
- Bin & Level Setup:
    - Entry: Starting Bin
    - Entry: Ending Bin
    - Dropdown: (Odd, Even, Both)
    - Entry: Starting Level
    - Entry: Ending Level
    - Entry: Size
    - Entry: Storage Code
    - Confirm Button
        - When confirm button is hit, display a popup stating that this will overrite any information currently in the system about this aisle.

- Display Aisle: 
    - Show each Zone, and the current Setup

### CUI - Create User ID
Allows the creation and setup of User IDs, grants permissions, changes passwords, 

- Enter User ID
    - Once USer ID is entered, other information populates
- Employee Name
- Employee Department
- Dropdown with Permissions
- Password (Marked with *s)

### CHL - Clear Hung Location
Forces a full clear of a location in case something happens that causes the system to glitch and not allow anything to go to a location (used in cases when a location systematically cannot be cleared for some reason.  Deletes the locatino and then re-adds it).

- Aisle
- Bin
- Level
- Confirm
    - Searches that location in the database.
    - Deletes any Pallet ID in that location from the Pallets Database
    - Deletes any information about this location from the locations database except aisle, bin, level, size, and storage code.



## Database Designs

### User Database
| Key        | Data Type | Additional Info|
|:-----------|:---------:|:---------------|
| UserID     | TEXT      | Primary Key
| UserName   | TEXT      |
| Password   | TEXT      | Hashed
| Role       | TEXT      |
| Department | TEXT      |


### Pallet Information
| Key        | Data Type | Additional Info|
|:-----------|:---------:|:---------------|
| PalletID   | TEXT      | PRIMARY KEY
| ItemID     | TEXT      | FOREIGN KEY (Item Table)
| Quantity   | INTEGER   |
| VCP        | INTEGER   |
| SSP        | INTEGER   |
| PalletSize | TEXT      | (Linked to Location)
| StorageCode| TEXT      | (Linked to Item ID)
| LocationID | TEXT      | FOREIGN KEY (Locations Table)
| ExpireDate | TEXT      |
| Status     | TEXT      | 
| CreateDate | TEXT      | 
| CreateID   | TEXT      | FOREIGN KEY (User Table)
| PutDate    | TEXT      |
| PutID      | TEXT      | FOREIGN KEY (User Table)
| PullDate   | TEXT      |
| PullID     | TEXT      | FOREIGN KEY (User Table)

### Location Information

| Key        | Data Type | Additional Info|
|:-----------|:---------:|:---------------|
| Aisle      | TEXT      | 3 digits exactly
| Bin        | TEXT      | 3 digits exactly
| Level      | TEXT      | 2 digits exactly
| LocationID | TEXT      | PRIMARY KEY (Composite of AisleBinLevel)
| StorageCode| TEXT      | FOREIGN KEY (StorageCodes Table)
| Size       | TEXT      |

### Storage Codes

| Key        | Data Type | Additional Info|
|:-----------|:---------:|:---------------|
| StorageCode| TEXT      | PRIMARY KEY
| StorageType| TEXT      |

### Item Information

| Key        | Data Type | Additional Info|
|:-----------|:---------:|:---------------|
| Dept       | TEXT      | 3 digits exactly
| Class      | TEXT      | 2 digits exactly
| Item       | TEXT      | 4 digits exactly
| ItemID     | TEXT      | PRIMARY KEY (Composit of DeptClassItem)
| Name       | TEXT      |
| Description| TEXT      |
| StorageCode| TEXT      |
| VCP        | INTEGER   |
| SSP        | INTEGER   |
| Cost       | FLOAT     |
| Price      | FLOAT     |
