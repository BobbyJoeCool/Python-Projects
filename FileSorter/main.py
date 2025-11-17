# Entry point for the File Sorter and Re-namer program

import os
import funcs

def main():
    folder = funcs.getFolder()
    if folder:
        fileDict = funcs.fileDictionary(folder)
        funcs.moveFiles(fileDict, folder)
        print(f"\nFiles moved successfully")

if __name__ == "__main__":
    main()