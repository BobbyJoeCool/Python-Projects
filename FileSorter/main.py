# Entry point for the File Sorter and Re-namer program

import os
from utils import get_user_directory, setup_logging
from sorter import sort_files

def main():
    # Step 1: Initialize log system
    setup_logging()

    # Step 2: Ask user for directory to organize
    target_dir = get_user_directory()

    # Step 3: Confirm the path exists
    if not os.path.exists(target_dir):
        print("Error: Directory not found.")
        return

    # Step 4: Call the sorter logic
    sort_files(target_dir)

    print("\nSorting complete! Check the 'logs/sorter.log' file for details.")

if __name__ == "__main__":
    main()