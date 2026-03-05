"""Business logic layer for the Work Job Tracker application.

This module contains domain-level rules and orchestration code that should not
live inside:
- The GUI layer (Tkinter)
- The DB layer (SQL)

Responsibilities:
- Authenticate users and construct User objects
- Normalize and validate report date ranges
- Translate GUI options into DB query parameters
- Provide thin service functions that the GUI can call
"""

from __future__ import annotations

from datetime import date, datetime, time

import db
import mysql.connector
from models import (
    AbsentShifts,
    ShiftByDateRow,
    ShiftByEquipment,
    ShiftByFunction,
    ShiftLogRow,
    TimeSince,
)
from tools import timeDifference
from user import User


def authenticate(
    username: str, password: str
) -> tuple[mysql.connector.MySQLConnection, User]:
    """Authenticate a user and return a DB connection plus a User object.

    Args:
        username: The username entered by the user.
        password: The password entered by the user.

    Return:
        conn: A MySQL Connection object.
        user: A User dataclass containing the authenticated username.
    """

    conn = db.getConn(username, password)
    # TODO: Load user roles/permissions from DB and attach to the User model.
    return conn, User(zNumber=username)


def normalize_dates(
    startDate: date | None, endDate: date | None
) -> tuple[datetime, datetime]:
    """Normalize optional start/end dates into inclusive datetime bounds.

    Args:
        startDate: Optional start date.
        endDate: Optional end date.

    Return:
        startDate: Start datetime at 00:00:00 of startDate (default 2025-01-01).
        endDate: End datetime at 23:59:59.999999 of endDate (default today).
    """

    if startDate is None:
        # TODO: Replace magic default date with a configurable constant.
        startDate = date(2025, 1, 1)
    if endDate is None:
        endDate = date.today()

    start_dt = datetime.combine(startDate, time.min)
    end_dt = datetime.combine(endDate, time.max)

    return start_dt, end_dt


def get_shift_ids(home: bool = True, overtime: bool = True) -> list[str]:
    """Convert GUI shift selections into ShiftID values.

    Args:
        home: Whether the home shift selection is enabled.
        overtime: Whether the overtime shift selection is enabled.

    Return:
        shiftIDs: A list of shift IDs (e.g., ["B1", "A1"]).
    """

    shiftIDs: list[str] = []

    if home:
        shiftIDs.append("B1")
    if overtime:
        shiftIDs.append("A1")

    return shiftIDs


def evaluate_shift_duration(
    startTime: datetime, endTime: datetime
) -> tuple[float, bool, bool]:
    """Compute a shift duration and classify it for UI confirmation.

    Args:
        startTime: The shift start datetime.
        endTime: The shift end datetime.

    Return:
        hours: Shift duration in hours.
        isZero: True if the shift duration is 0 hours.
        isLong: True if the shift duration is greater than 12 hours.
    """

    hours = timeDifference(startTime, endTime)
    isZero = hours == 0
    isLong = hours > 12
    return hours, isZero, isLong


def get_jobs(conn: mysql.connector.MySQLConnection) -> dict[str, int]:
    """Retrieve the job selection mapping for GUI display.

    Args:
        conn: mySQL Connection object.

    Return:
        jobMap: Dictionary mapping display labels to JobFunction IDs.
    """

    return db.getJobs(conn)


def get_shifts(conn: mysql.connector.MySQLConnection) -> list[str]:
    """Retrieve the list of valid shift keys.

    Args:
        conn: mySQL Connection object.

    Return:
        shifts: List of ShiftID values.
    """

    return db.getShifts(conn)


def log_shift(
    conn: mysql.connector.MySQLConnection,
    user: User,
    startTime: datetime,
    endTime: datetime,
    key: str,
    functionName: str,
) -> None:
    """Log a shift for the active user.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        startTime: Shift start datetime.
        endTime: Shift end datetime.
        key: Shift key (ShiftID).
        functionName: Name of the job function.

    Return:
        None
    """

    db.logShift(conn, user.zNumber, startTime, endTime, key, functionName)


def report_shifts_by_date(
    conn: mysql.connector.MySQLConnection,
    user: User,
    home: bool,
    overtime: bool,
    absent: bool,
    startDate: date | None,
    endDate: date | None,
) -> tuple[str, tuple[tuple[str, str], ...], list[ShiftByDateRow]]:
    """Generate the Shifts-by-Date report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        home: Whether to include home shifts.
        overtime: Whether to include overtime shifts.
        absent: Whether to include absences.
        startDate: Optional start date.
        endDate: Optional end date.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    # TODO: Allow managers/admins to report on other users (multi Z-number support).
    start_dt, end_dt = normalize_dates(startDate, endDate)
    shiftIDs = get_shift_ids(home, overtime)
    return db.getShiftsByDate(conn, user.zNumber, shiftIDs, absent, start_dt, end_dt)


def report_shifts_by_function(
    conn: mysql.connector.MySQLConnection,
    user: User,
    home: bool,
    overtime: bool,
) -> tuple[str, tuple[tuple[str, str], ...], list[ShiftByFunction]]:
    """Generate the Shifts-by-Function report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        home: Whether to include home shifts.
        overtime: Whether to include overtime shifts.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    shiftIDs = get_shift_ids(home, overtime)
    return db.getShiftsByFunction(conn, user.zNumber, shiftIDs)


def report_shifts_by_equipment(
    conn: mysql.connector.MySQLConnection,
    user: User,
    home: bool,
    overtime: bool,
) -> tuple[str, tuple[tuple[str, str], ...], list[ShiftByEquipment]]:
    """Generate the Shifts-by-Equipment report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        home: Whether to include home shifts.
        overtime: Whether to include overtime shifts.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    shiftIDs = get_shift_ids(home, overtime)
    return db.getShiftsByEquipment(conn, user.zNumber, shiftIDs)


def report_time_since_functions(
    conn: mysql.connector.MySQLConnection,
    user: User,
    home: bool,
    overtime: bool,
) -> tuple[str, tuple[tuple[str, str], ...], list[TimeSince]]:
    """Generate the Time-Since-Function report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        home: Whether to include home shifts.
        overtime: Whether to include overtime shifts.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    shiftIDs = get_shift_ids(home, overtime)
    return db.timeSinceFunction(conn, user.zNumber, shiftIDs)


def report_absences(
    conn: mysql.connector.MySQLConnection,
    user: User,
    startDate: date | None,
    endDate: date | None,
) -> tuple[str, list[tuple[str, str]], list[AbsentShifts]]:
    """Generate the Absences report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        startDate: Optional start date.
        endDate: Optional end date.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    start_dt, end_dt = normalize_dates(startDate, endDate)
    return db.getMissedShifts(conn, user.zNumber, start_dt, end_dt)


def report_accountable_time(
    conn: mysql.connector.MySQLConnection,
    user: User,
    startDate: date | None,
    endDate: date | None,
) -> tuple[str, list[tuple[str, str]], list[AbsentShifts]]:
    """Generate the Accountable Time report.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        startDate: Optional start date.
        endDate: Optional end date.

    Return:
        name: User display name.
        headers: Header definitions.
        data: Dataclass rows for the report.
    """

    start_dt, end_dt = normalize_dates(startDate, endDate)
    return db.getAccountableShifts(conn, user.zNumber, start_dt, end_dt)


# Re-export DB-layer exception so the GUI does not import db directly.
InvalidLoginError = db.InvalidLoginError


def get_shift_log_pk(
    conn: mysql.connector.MySQLConnection,
    user: User,
    shiftStart: datetime,
    shiftEnd: datetime,
) -> int | None:
    """Get the ShiftLog primary key for a specific shift entry.

    Args:
        conn: mySQL Connection object.
        user: Authenticated user context.
        shiftStart: Shift start datetime.
        shiftEnd: Shift end datetime.

    Return:
        shiftID: The primary key ID for the ShiftLog row, or None if not found.
    """

    return db.getShiftLogPK(conn, user.zNumber, shiftStart, shiftEnd)


def get_shift_log_row(
    conn: mysql.connector.MySQLConnection,
    shiftID: int,
) -> ShiftLogRow | None:
    """Get a ShiftLogRow dataclass for a ShiftLog primary key.

    Args:
        conn: mySQL Connection object.
        shiftID: ShiftLog primary key.

    Return:
        row: A ShiftLogRow dataclass, or None if not found.
    """

    return db.getShiftLogRow(conn, shiftID)


def delete_shift(conn: mysql.connector.MySQLConnection, shiftID: int) -> None:
    """Delete a shift by ShiftLog primary key.

    Args:
        conn: mySQL Connection object.
        shiftID: ShiftLog primary key.

    Return:
        None
    """

    db.deleteShift(conn, shiftID)


def edit_shift(
    conn: mysql.connector.MySQLConnection,
    shiftID: int,
    shiftStart: datetime | None = None,
    shiftEnd: datetime | None = None,
    key: str | None = None,
    func: str | None = None,
    isAbsent: bool | None = None,
) -> None:
    """Edit a shift entry.

    Args:
        conn: mySQL Connection object.
        shiftID: ShiftLog primary key.
        shiftStart: Optional replacement shift start.
        shiftEnd: Optional replacement shift end.
        key: Optional replacement ShiftID.
        func: Optional replacement function name.
        isAbsent: Optional replacement absence flag.

    Return:
        None
    """

    db.editShift(conn, shiftID, shiftStart, shiftEnd, key, func, isAbsent)
