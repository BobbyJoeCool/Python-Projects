# Work Job Tracker

## Project Overview

The **Work Job Tracker** is a Python application designed to help employees track the jobs/functions they work during their shifts. All shift data is stored in a **MySQL database**, allowing for detailed reporting and analysis over time.

**Key Features:**
- ✅ Log hours worked for specific job functions via GUI
- ✅ Record shifts by date and shift key (B1 home, A1 overtime, etc.)
- ✅ Track employees by alphanumeric **Z-numbers**
- ✅ Generate reports: percent time per function, days since last function, shift summaries
- ✅ View shift history by date, function, and equipment
- ✅ Search and filter shifts with date range selection

This project combines **Python, Tkinter GUI, MySQL, and data analysis** in a real-world business context.

---

## Quick Start

### Prerequisites
- **Python 3.8+**
- **MySQL Server** (5.7+) running locally or remotely
- **pip** (Python package manager)

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <your-repo-url>
   cd Python-Projects/Work_Job_Tracker
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp setup.env.sample setup.env
   ```
   Edit `setup.env` with your MySQL credentials:
   ```
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=work_job_tracker
   ```

5. **Initialize the database**
   ```bash
   mysql -u your_username -p < database_create.sql
   ```
   Or use MySQL Workbench to run the SQL script against your database.

### Running the Application

```bash
python -m Work_Job_Tracker
```

The Tkinter GUI window will open with two tabs: **Log Shift** and **Reports**.

---

## Project Structure

```
Work_Job_Tracker/
├── __main__.py              # Entry point; opens database and launches GUI
├── __init__.py              # Package initialization
├── gui.py                   # Tkinter GUI (LogPage, ReportsPage, TimePicker)
├── db.py                    # MySQL database functions (queries, inserts, updates)
├── tools.py                 # Utilities (logging config, time calculations)
├── database_create.sql      # SQL schema and initial data
├── requirements.txt         # Python dependencies
├── setup.env                # Environment variables (DO NOT COMMIT)
├── setup.env.sample         # Template for setup.env
├── readme.md                # This file
├── Logs/                    # Application logs (op.log, debug.log)
└── __pycache__/             # Python bytecode cache
```

### Module Responsibilities

**main.py**
- Application entry point
- Initializes logging
- Connects to MySQL database
- Launches Tkinter GUI
- Manages graceful shutdown

**gui.py**
- Tkinter GUI implementation
- `LogPage`: Shift entry form with date/time pickers
- `ReportsPage`: Shift reports and analytics
- `TimePicker`: Custom time input widget

**db.py**
- All MySQL database operations
- Dataclasses for type-safe data handling
- Query functions: `getShiftsByDate()`, `getShiftsByFunction()`, `logShift()`, `deleteShift()`, etc.
- Employee and job function lookups

**tools.py**
- `configureLogging()`: Sets up logging to file and console
- `timeDifference()`: Calculates hours between two times (handles overnight shifts)
- `mysqlTimeToTime()`: Converts MySQL time objects to Python `time` objects

---

## Database Schema

The application uses three main tables (see `database_create.sql` for full schema):

### Employee
Stores employee information by Z-number.
```sql
CREATE TABLE Employee (
    ZNumber VARCHAR(10) PRIMARY KEY,
    Name VARCHAR(50) NOT NULL
);
```

### JobFunction
Available job functions employees can log.
```sql
CREATE TABLE JobFunction (
    FunctionID INT PRIMARY KEY AUTO_INCREMENT,
    FunctionName VARCHAR(100) NOT NULL,
    FunctionType VARCHAR(50)
);
```

### ShiftLog
Individual shift entries logged by employees.
```sql
CREATE TABLE ShiftLog (
    ShiftLogID INT PRIMARY KEY AUTO_INCREMENT,
    ZNumber VARCHAR(10) NOT NULL,
    FunctionID INT NOT NULL,
    TimeStarted DATETIME NOT NULL,
    TimeFinished DATETIME NOT NULL,
    ShiftID VARCHAR(10),
    IsAbsent BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (ZNumber) REFERENCES Employee(ZNumber),
    FOREIGN KEY (FunctionID) REFERENCES JobFunction(FunctionID)
);
```

Additional tables for equipment, absences, and shift definitions are included in `database_create.sql`.

---

## Features

### Logging Shifts (Log Shift Tab)
1. Select a **Job Function** from dropdown
2. Enter the **shift key** (e.g., B1, A1)
3. Pick **start time** and **end time** using date/time pickers
4. Click **Log Shift** to save to database
5. Confirm the entry in the popup dialog

**Validations:**
- Shifts cannot be 0 hours
- Warning if shift > 12 hours (requires confirmation)
- All fields required

### Reports (Reports Tab)
- **By Date**: View all shifts logged on a specific date
- **By Function**: See total hours and percent of time in each function
- **By Equipment**: Breakdown of equipment usage hours
- **Absent Shifts**: View scheduled but unworked shifts
- **Time Since**: Days since last worked in each function
- **Shift Summary**: View all shifts sorted by date or shift type

---

## Logging

The application logs to two files in the `Logs/` directory:

- **op.log**: Operational messages (INFO level and above)
- **debug.log**: Detailed debug messages (DEBUG level and above)

Logs are also printed to the console at INFO level.

Configure logging level in `tools.py` → `configureLogging()`.

---

## Development

### Code Quality
The project uses:
- **ruff**: Fast Python linter
- **black**: Code formatter
- **pre-commit**: Git hooks for automatic checks

Run checks manually:
```bash
ruff check .
black --check .
```

### Testing
Currently minimal testing. To add tests:
```bash
pip install pytest
pytest tests/
```

Start with unit tests for `tools.py` functions (e.g., `timeDifference()` for edge cases).

### Debugging
- Check logs in `Logs/` directory
- Enable DEBUG logging in `tools.py`
- Use the debug log (`debug.log`) for detailed tracebacks

---

## Troubleshooting

### "Database Connection Failed" on startup
- Verify MySQL is running: `mysql -u your_user -p`
- Check credentials in `setup.env`
- Verify database name matches `MYSQL_DATABASE` in setup.env
- Check logs in `Logs/debug.log`

### "No module named 'mysql.connector'"
```bash
pip install -r requirements.txt
```

### Shifts not appearing in reports
- Ensure shifts are logged for today's date
- Check the `ShiftLog` table in MySQL:
  ```sql
  SELECT * FROM ShiftLog ORDER BY TimeStarted DESC LIMIT 10;
  ```

### Time calculations look wrong
- Overnight shifts (e.g., 11 PM → 7 AM) should calculate correctly
- If not, check `timeDifference()` in `tools.py`

---

## Future Enhancements

Planned features (see `Outline for Improvement and Refactoring.md`):
- [ ] Multi-user login with role-based access
- [ ] Modify/split existing shifts (instead of delete/re-log)
- [ ] Date range filtering for reports
- [ ] Export reports to CSV/Excel
- [ ] Performance graphs and trend analysis
- [ ] Unit and integration tests
- [ ] Docker containerization for MySQL

---

## Contributing

To contribute:
1. Create a branch: `git checkout -b feature/your-feature`
2. Make changes and test locally
3. Run linters: `ruff check .` and `black .`
4. Commit: `git commit -m "Add feature: description"`
5. Push and open a pull request

---

## License

This project is for internal use. See LICENSE file for details.

---

## Support

For issues, questions, or suggestions:
- Check the logs in `Logs/debug.log`
- Review the Database Schema section above
- See `Outline for Improvement and Refactoring.md` for planned fixes