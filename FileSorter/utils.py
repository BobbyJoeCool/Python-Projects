# Helper functions for input validation and logging setup

import os
import logging

def setup_logging():
    """
    Configures the logging system to write to logs/sorter.log
    """
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/sorter.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def get_user_directory():
    """
    Prompts the user for a directory path to organize.
    """
    print("Enter the full path of the directory to organize:")
    return input("> ").strip()