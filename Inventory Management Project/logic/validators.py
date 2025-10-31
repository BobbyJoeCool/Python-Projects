    # Validation Functions
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