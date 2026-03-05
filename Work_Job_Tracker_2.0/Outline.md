# Work Job Tracker - Project Architecture

This document provides a high-level overview of the Python Work Job Tracker project, showing the modules and how they interact with each other and the database.

## Module Responsibilities

### main

- Entry point of the program
- Configures the Database, opens the connections and passes the cursor and database to the GUI
- Opens the GUI for the user
- Closes the database

### db

- Handles all database funtions - logging shifts and retrieving data from the database 
- Handles queries such as retrieving data from the database for the UI and helper functions (getting the PK for job functions, employees, etc.  
- Handles Getting a list of job functions for the user to select from.)

### utils

- Helper Functions: takes data from user input and converts it into data for the database.
- Helper Functions: takes data from the database and converts it into useful information (takes figures out the time in functions for example).

### gui

- Handles user input
- Displays to the user information requested.
- Tkinter Interface