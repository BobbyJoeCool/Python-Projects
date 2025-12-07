# Work Shift Tracker

## Project Overview

The **Work Shift Tracker** is a Python application designed to help employees track the jobs/functions they work during their shifts. All shift data is stored in a **MySQL database**, allowing for detailed reporting and analysis over time.

Key features include:

- Logging hours worked for specific job functions.
- Recording shifts by date and key (B1 home key, or A1 overtime).
- Storing employee IDs using alphanumeric **Z numbers**.
- Generating reports such as:
  - Percent time spent in each function.
  - Days since last worked in each function.
  - Sorting shifts by day of the week or shift type.

This project provides a practical example of combining **Python, MySQL, and data analysis** in a real-world context.

---

## Database Schema

### Employee Table

Stores employees using alphanumeric Z numbers.

```sql
CREATE TABLE Employee (
    ZNumber VARCHAR(10) PRIMARY KEY,  
    Name VARCHAR(50)
);

CREATE TABLE JobFunction (
    FunctionID INT PRIMARY KEY AUTO_INCREMENT,
    FunctionName VARCHAR(50) NOT NULL
);

CREATE TABLE ShiftLog (
    ShiftID INT PRIMARY KEY AUTO_INCREMENT,
    ZNumber VARCHAR(10),
    FunctionID INT,
    DateWorked DATE,
    HoursWorked DECIMAL(4,2),
    ShiftType VARCHAR(20),
    FOREIGN KEY (ZNumber) REFERENCES Employee(ZNumber),
    FOREIGN KEY (FunctionID) REFERENCES JobFunction(FunctionID)
);
```

## Planned Features

1. GUI Interface: Build a Tkinter-based form for logging shifts.
1. Advanced Analytics:
    - Graphs for percent time in each function.
    - Trend analysis for days worked per function or shift.
1. Multiple Employees: Track a team, not just one individual.
1. Export Options: CSV/Excel export for reporting.