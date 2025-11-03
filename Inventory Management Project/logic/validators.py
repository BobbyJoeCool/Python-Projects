# ---------Validation Functions----------
def PID(pid):
    if pid != "":
        return True
    else:
        return False
        
def LabelID(labelID):
    if labelID != "":
        return True
    else:
        return False
        
def Aisle(aisle):
    if len(aisle) == 3:
        return True
    else:
        return False
    
def Location(location):
    if len(location) == 8:
        return True
    else:
        return False
    
def PullCode(pullCode):
    if pullCode.upper() in ("CA", "FP", "BK"):
        return True
    else:
        return False
    
def StorageCode(storageCode):
    if storageCode.upper() in ("CR", "FD", "NR", "NF"):
        return True
    else:
        return False
    
def Size(size):
    if size.upper() in ("HS", "S", "M", "L"):
        return True
    else:
        return False