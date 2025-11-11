# ---------Validation Functions----------
import sqlite3

dbPATH = "IMS/database/database.db"

def getConn():
    db = sqlite3.connect(dbPATH)
    db.row_factory = sqlite3.Row
    cur = db.cursor()
    return db, cur

def PID(pid):
    db, cur = getConn()
    cur.execute("SELECT 1 FROM pallet WHERE PalletID = ?", (pid,))
    exists = cur.fetchone()
    db.close()
    return bool(exists)
        
def LabelID(labelID):
    if labelID != "":
        return True
    else:
        return False
        
def Aisle(aisle):
    db, cur = getConn()
    cur.execute("SELECT 1 FROM locations WHERE Aisle = ?", (aisle,))
    exists = cur.fetchone()
    db.close()
    return bool(exists)
    
def LocationExists(aisle, bin, level):
    db, cur = getConn()
    cur.execute("SELECT 1 FROM locations WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
    exists = cur.fetchone() is not None
    db.close()
    return bool(exists)

def LocationEmpty(aisle, bin, level):
    exists = LocationExists(aisle, bin, level)
    if exists:
        db, cur = getConn()
        cur.execute("SELECT Status FROM locations WHERE Aisle = ? AND Bin = ? AND Level = ?", (aisle, bin, level))
        result = cur.fetchone()
        db.close()
        return result == "Empty"
    
def PullCode(pullCode):
    if pullCode.upper() in ("CA", "FP", "BK"):
        return True
    else:
        return False
    
def StorageCode(storageCode):
    db, cur = getConn()
    cur.execute("SELECT 1 FROM storageCode WHERE StorageCode = ?", (storageCode,))
    exists = cur.fetchone()
    db.close()
    return bool(exists)
    
def Size(size):
    if size.upper() in ("HS", "S", "M", "L"):
        return True
    else:
        return False
    
def UserID(userID):
    db, cur = getConn()
    cur.execute("SELECT 1 FROM users WHERE UserID = ?", (userID,))
    exists = cur.fetchone()
    db.close()
    return bool(exists)

def Login(userID, password):
    db, cur = getConn()
    cur.execute("SELECT * from users WHERE userID = ?", (userID,))
    result = cur.fetchone()
    if not result:
        return False
    validLogin = password == result["Password"]
    db.close()
    return validLogin, result["UserName"]
