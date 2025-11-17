from datetime import datetime
import os

baseFolder = os.getcwd()
logDir = os.path.join(baseFolder, "Logs")
os.makedirs(logDir, exist_ok=True)

def createLog():
    logFileName = datetime.now().strftime("session_%Y-%m-%d_%H-%M-%S.txt")
    logPath = os.path.join(logDir, logFileName)
    with open(logPath, "w") as logFile:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logFile.write(f"Files moves at: {timestamp}\n\n")
    return logPath

def writeLog(logPath, fileName, folderName, status="moved"):
    with open(logPath, "a") as logFile:
        logFile.write(f"[{fileName} -> {folderName}] ({status})\n")