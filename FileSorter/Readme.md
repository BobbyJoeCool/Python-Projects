# File Sorter

A Python automation tool that organizes files in a folder into categorized subfolders.

## Features

- Automatically sorts files by extension (images, documents, etc.)
- Logs actions and errors
- Easily customizable categories via `config.py`

## Usage

1. Run `python main.py`
2. Enter the folder path you want to organize
3. Check `logs/sorter.log` for results

## File Structure

Readme.file_sorter/

    - main.py          # Entry point of the program
    - sorter.py        # Core logic for sorting and moving files
    - config.py        # Contains category definitions and paths
    - utils.py         # Helper functions (logging, validation, etc.)
    - logs/
        - sorter.log   # Program logs (created automatically)
    - README.md        # Optional documentation for project
