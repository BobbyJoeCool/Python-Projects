# sorter.py
# Handles categorizing and moving files to their appropriate folders

import os
import shutil
import logging

def sort_files(directory):
    """
    Main function to organize files inside the specified directory.
    """
    logging.info(f"Starting file sort in: {directory}")

    # Step 1: Loop through all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Step 2: Skip subfolders
        if os.path.isdir(file_path):
            continue

        # Step 3: Extract the file extension (e.g., .jpg, .pdf)
        file_ext = os.path.splitext(filename)[1].lower()

        # Step 4: Determine category (default = "Other")
        category = get_category(file_ext)

        # Step 5: Build destination path and move the file
        dest_folder = os.path.join(directory, category)
        os.makedirs(dest_folder, exist_ok=True)

        try:
            shutil.move(file_path, os.path.join(dest_folder, filename))
            logging.info(f"Moved: {filename} → {category}")
        except Exception as e:
            logging.error(f"Failed to move {filename}: {e}")

    logging.info("Sorting complete.")

def get_category(extension):
    """
    Returns the category name for a given file extension.
    """
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Other"