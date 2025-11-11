import sqlite3
import logic.validators as val

# Database path
dbPATH = "IMS/database/database.db"

# ---------- Database Connection ----------
def getConn():
    # Returns a database connection and cursor with row access as dictionary
    db = sqlite3.connect(dbPATH)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    return db, cur

# ---------- Pallet Table Functions ----------
def GetPalletInfo(PID):
    # Return the entire pallet row as a dictionary
    db, cur = getConn()
    cur.execute("SELECT * FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def PIDgetDPCI(PID):
    # Return Dept, Class, Item as a dict
    db, cur = getConn()
    cur.execute("SELECT Dept, Class, Item FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def PIDgetQuantity(PID):
    # Return Quantity as int
    db, cur = getConn()
    cur.execute("SELECT Quantity FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def PIDgetSize(PID):
    # Return Size as str
    db, cur = getConn()
    cur.execute("SELECT Size FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def PIDgetLocation(PID):
    # Return Aisle, Bin, Level as dict
    db, cur = getConn()
    cur.execute("SELECT Aisle, Bin, Level FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def PIDgetStatus(PID):
    # Return Status as str
    db, cur = getConn()
    cur.execute("SELECT Status FROM pallet WHERE PalletID = ?", (PID,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def LocGetPallet(aisle, bin, level):
    # Returns Pallet Information if stored in a location as dict.
    db, cur = getConn()
    cur.execute("SELECT * FROM pallet WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None


# ---------- Items Table Functions ----------
def GetItemInfo(dept, cls, item):
    # Return entire item row as dict
    db, cur = getConn()
    cur.execute("SELECT * FROM items WHERE Dept = ? AND Class = ? AND Item = ?", (dept, cls, item))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def DPCIgetName(dept, cls, item):
    # Return item Name as str
    db, cur = getConn()
    cur.execute("SELECT Name FROM items WHERE Dept = ? AND Class = ? AND Item = ?", (dept, cls, item))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

# ---------- StorageCodes Table Functions ----------
def StorageExpires(storageCode):
    # Return Expire as bool (0 or 1)
    db, cur = getConn()
    cur.execute("SELECT Expire FROM storageCodes WHERE StorageCode = ?", (storageCode,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def StorageRestricted(storageCode):
    # Return Restricted as bool (0 or 1)
    db, cur = getConn()
    cur.execute("SELECT Restricted FROM storageCodes WHERE StorageCode = ?", (storageCode,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

# ---------- Locations Table Functions ----------
def GetLocationInfo(aisle, bin, level):
    # Return entire location row as dict
    db, cur = getConn()
    cur.execute("SELECT * FROM locations WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def LocGetStatus(aisle, bin, level):
    # Return location Status as str
    db, cur = getConn()
    cur.execute("SELECT Status FROM locations WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def LocGetStorage(aisle, bin, level):
    # Return StorageCode as str
    db, cur = getConn()
    cur.execute("SELECT StorageCode FROM locations WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

# ---------- Users Table Functions ----------
def GetUserInfo(userID):
    # Return entire user row as dict
    db, cur = getConn()
    cur.execute("SELECT * FROM users WHERE UserID = ?", (userID,))
    row = cur.fetchone()
    db.close()
    return dict(row) if row else None

def UserGetRole(userID):
    # Return Role as str
    db, cur = getConn()
    cur.execute("SELECT Role FROM users WHERE UserID = ?", (userID,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None

def UserGetName(userID):
    # Return UserName as str
    db, cur = getConn()
    cur.execute("SELECT UserName FROM users WHERE UserID = ?", (userID,))
    row = cur.fetchone()
    db.close()
    return row[0] if row else None