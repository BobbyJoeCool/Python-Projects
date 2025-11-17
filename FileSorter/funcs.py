# sorter.py
# Handles categorizing and moving files to their appropriate folders

import os
import shutil
import logger

def getFolder():
    while True:
        folder = input("Enter a path to your folder (enter "" to quit):")
        if folder == "":
            return None
        if os.path.exists(folder):
            print("Path exists!")
            print("Directory Contents:")
            for item in os.listdir(folder):
                print(item)
            response = input(f"\nIs this the folder you wish to sort? (y/n)")
            if response[0].lower() == "y":
                return folder
        else:
            print("Path does NOT exist.  Please Try Again.")

def fileDictionary(folder):
    files = {}
    for item in os.listdir(folder):
        full_path = os.path.join(folder, item)

        if os.path.isdir(full_path):
            continue

        _, ext = os.path.splitext(item)
        ext = ext.lower()

        files.setdefault(ext, []).append(item)

    return files

def moveFiles(files, folder):
    logPath = logger.createLog()
    for ext, fileList in files.items():
        folderName = ext.lstrip(".") if ext else "MISC"
        destFolder = os.path.join(folder, folderName)
        os.makedirs(destFolder, exist_ok=True)
        for f in fileList:
            source = os.path.join(folder, f)
            dest = os.path.join(destFolder, f)

            if os.path.exists(source):
                shutil.move(source, dest)
                logger.writeLog(logPath, f, folderName)
            else:
                logger.writeLog(logPath, f, folderName, status="not found")
