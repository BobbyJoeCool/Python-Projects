## New Features to Add

- [ ] Added Functionality for additional Z-Numbers (currently hardcoded to one ZNumber)
- [x] Add a login screen to manage who is accessing the system (including the ZNumber which will be used to determine who's shifts get pulled from the database)
- [ ] Add roles for users, including users, managers, and an admin.  Managers will be able to add users to the database.  Users will have all the shift editing and reporting functions for their zNumber only.  Managers will be able to add and edit shifts for all users as well as have access to reports that invlove all users.  Admins will be able to add users to the database and grant access based on user roles.
- [x] Add a way to modify already logged shifts, including splitting an already existing shift, rather than having to delete and re-log the shift.
- [x] Add a function to show how many days/shifts it's been since a function has been performed.
- [x] Add the ability to set a date range for the database lookup.
- [x] Combine the date/time into a datetime object for the database (may require some refactoring of the database).

## Quick, High-Priority Fixes

- [x] Hard-coded user ID: gui.py calls db.logShift(conn, "z002p25", ...) and db.deleteShift uses "z002p25" — make the Z-number configurable (selectable in UI or from config). See gui.py.
- [x] Use instance conn, not module global: Many ReportsPage / LogPage methods call db functions with the bare name conn instead of self.conn. This will break when conn is not a module-level global — switch to self.conn. See gui.py.
- [x] Replace prints with logging: db.py and main.py use print() for errors/status. Use the logging module and configure it in one place (e.g., Work_Job_Tracker/__init__.py or utils.py).
- [x] Protect DB secrets: setup.env is read directly; ensure .env/setup.env is listed in .gitignore and provide setup.env.sample. Prefer environment variables or secrets manager.

## Correctness & Bug Risks

- [x] Suspicious argument handling: getShiftsByFunction and getShiftsByEquipment ignore passed startDate/endDate (overrides them). Review and fix parameter usage in db.py.
- [x] SQL string building: cleanEntry returns SQL fragment strings assembled into f-strings. This works but is fragile; prefer explicit parameterized SQL construction or a small query builder to avoid malformed SQL in edge cases.
- [ ] Magic/default dates: cleanEntry and getMissedShifts use hard-coded date(2025,1,1) — make a configurable constant or use a semantic default (e.g., epoch or earliest available date).
- [x] Cursor/context management: Use context managers for cursors (and optionally connection pooling). e.g., with conn.cursor() as cur: so cursors always close on exceptions.
- [x] Exception handling breadth: Some broad excepts (except Error as e:) print and continue; make errors clearer and handle known exceptions separately (integrity, connection errors).


## API / Structure Improvements

- [ ] Separate UI vs business logic: Move all business logic (calls transforming DB rows, time calculations) out of gui.py into logic/ (or services/) so UI is thin and testable. E.g., data formatting in getShiftsByDate could be split into DB fetch + formatter.
- [x] Return typed data structures: DB functions return lists of lists; consider returning dataclass objects or dicts for readability and type hints.
- [x] Module/package layout: Convert Work_Job_Tracker into a proper package (__init__.py) and expose a main() entrypoint. Add a console script in pyproject.toml if packaging.


## UX & Robustness

- [ ] Input validation: TimePicker.getTime() assumes hour/minute parse to int; add safe parsing and user feedback in the UI. Also validate DateEntry values and required selections (e.g., job selected).
- [x] Graceful DB failure UI: If getConn() returns None, main.py currently does nothing. Show a UI error dialog or fall back to offline mode rather than silent failure.
- [x] Treeview column handling: clearTreeview sets column widths to 0 and clears headings; consider destroying/creating columns or using tree["displaycolumns"] for clearer behavior.

## Code Quality & Style

- [x] Apply formatters/linters: Add black, isort, and ruff/flake8 to the repo and run them. Many files would benefit from consistent style.
- [x] Type hints and docstrings: Add type annotations to DB functions and 
- [ ] GUI methods; add module/class docstrings.
- [ ] Unit tests for utils.py: Add pytest tests for timeDifference() and mysqlTimeToTime() to validate boundary cases (overnight shifts).


## Security & Configuration

- [x] Don't commit secrets: Add setup.env to .gitignore. Add setup.env.sample with placeholders. Use python-dotenv only for local dev.
- [x] Parameterize DB config: Allow DB host/port/name/user via env vars and fail early with clear errors when missing.
- [x] Use parameterized SQL everywhere: You're already using %s placeholders, good — keep that pattern and avoid injecting any user strings into SQL fragments.


## DB & Data Handling

- [ ] Migrations & schema management: The repo has database_create.sql — add a simple migration approach (timestamped SQL scripts or a tiny migration runner), or adopt Alembic for long-term.
- [ ] Test DB or fixtures: Provide a lightweight SQLite fallback for tests or provide local MySQL docker-compose setup for CI tests.
- [ ] Transaction management: Wrap multi-statement changes in transactions or explicitly handle rollbacks on failure.


## Developer Experience

- [x] Add requirements.txt / pyproject.toml: Pin tkcalendar, mysql-connector-python, python-dotenv, etc.
- [X] Add .gitignore and pre-commit: Enforce formatting and linting locally.
- [x] Add per-subproject README: Expand readme.md with run steps, env setup, and how to populate DB (use database_create.sql).
- [x] Add CI: A GitHub Actions workflow to run ruff/black/pytest on PRs.


## Testing & CI

- [ ] Unit tests: Start with utils.py and db query builders (mock DB connection with pytest-mock or unittest.mock).
- [ ] Integration tests: Add an optional integration test that runs against a disposable MySQL (or docker) in CI.
- [ ] Run GUI smoke test: Minimal end-to-end check that main() instantiates GUI with a mocked conn.


## Prioritized Implementation Plan (suggested)

- [x] Short-term (day): 
    - [x] Add .gitignore, requirements.txt, setup.env.sample
    - [x] replace printed secrets
    - [x] stop hard-coding Z-number (UI select).
- [ ] Short-term (week): 
    - [x] Fix conn usage in gui.py methods
    - [x] add logging
    - [x] add cursor context managers
    - [ ] add basic tests for utils.py.
- [ ] Medium-term (2–4 weeks): 
    - [ ] Split UI/business logic
    - [x] add type hints
    - [x] configure pre-commit
    - [x] add CI workflow.
- [ ] Long-term: Migrations, packaging (pyproject.toml), integration tests with a disposable DB, and optional refactor to ORM if DB complexity grows.
