"""
Database access layer for the Work Job Tracker application.

This module contains all MySQL database functions related to:
- Shift Logging and Editing
- Employee shift queries and reports
- Job Function and Equipment Summaries

All functions assume an active MySQL connection and return 
data formatted for GUI consumption.
"""

import logging
import os
from datetime import date, datetime

import mysql.connector
from dotenv import dotenv_values
from models import (
    AbsentShifts,
    ShiftByDateRow,
    ShiftByEquipment,
    ShiftByFunction,
    ShiftLogRow,
    TimeSince,
)
from mysql.connector import Error, errorcode
from tools import configureLogging, timeDifference

logger = logging.getLogger("db.py")

# TODO: Add schema migration tooling (timestamped SQL scripts or Alembic).
# TODO: Provide a lightweight test DB/fixtures (SQLite or MySQL docker) for CI.
# TODO: Add integration tests that run against a disposable MySQL instance.


class InvalidLoginError(Exception):
    """Raised when the database authentication fails."""

    pass


def _shift_id_clause(shiftIDs: list[str]) -> tuple[str, list[str]]:
    """Build a SQL clause and parameters for filtering ShiftID values.

    Args:
        shiftIDs: List of shift IDs to include (e.g., ["B1", "A1"]).

    Returns:
        A tuple of (clause, params) where clause is an SQL fragment and params
        are the shift IDs for parameterized queries.

    Note:
        If shiftIDs is empty, the clause will filter to no rows.
    """

    if shiftIDs:
        placeholders = ", ".join(["%s"] * len(shiftIDs))
        return f"AND s.ShiftID IN ({placeholders})", shiftIDs
    return "AND 1=0", []


def getConn(user: str, password: str) -> mysql.connector.MySQLConnection:
    """
    Gets the connection to the Database.

    Args:
        user: Users entered Username
        password: Users entered Password

    Return:
        conn: A MySQL Connection object.
    """

    baseDir = os.path.dirname(os.path.abspath(__file__))
    envPath = os.path.join(baseDir, "setup.env")
    setup = dotenv_values(envPath)

    config = {
        "host": setup["DB_HOST"],
        "user": user,
        "password": password,
        "database": setup["DB_NAME"],
        "raise_on_warnings": True,
    }

    try:
        conn = mysql.connector.connect(**config)
        if not conn.is_connected():
            logger.error("Could not connect to database: %s", config)
            raise InvalidLoginError("MySQL access denied for user")
        return conn

    except Error as e:
        logger.error("Error: %s", e)

        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise InvalidLoginError("MySQL access denied for user")

        raise


def getShiftLogPK(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    shiftStart: datetime,
    shiftEnd: datetime,
) -> int | None:
    """
    This function takes the unique identifier for a shiftLog
    and gets the Primary Key.

    Args:
        conn: mySQL Connection Object
        zNumber: the users zNumber
        shiftStart: the datetime object for the shift start
        shiftEnd: the datetime object for the shift end

    Return:
        row[0]: Primary Key for Shift with those arguments
        or None if the shift doesn't exist.
    """

    with conn.cursor() as cur:
        cur.execute(
            """SELECT ID
            FROM ShiftLog
            WHERE ZNumber = %s
            AND TimeStarted = %s
            AND TimeFinished = %s""",
            (zNumber, shiftStart, shiftEnd),
        )
        row = cur.fetchone()
    return row[0] if row else None


def getShiftLogRow(
    conn: mysql.connector.MySQLConnection, ID: int
) -> ShiftLogRow | None:
    """
    This function gets the information for a shift from the primary Key.

    Args:
        conn: mySQL Connector Object
        ID: the ShiftLog Primary Key.

    Returns:
        row: A dataclass with the row with all the shift information
        or None if the primary key is not found.
    """
    logger.debug("Passed Shift ID: %s", ID)
    with conn.cursor(dictionary=True) as cur:
        cur.execute(
            """SELECT 
                s.ID,
                s.ZNumber,
                s.FunctionID,
                s.TimeStarted,
                s.TimeFinished,
                s.ShiftID,
                s.IsAbsent,
                f.Name AS FuncName,
                f.Type AS FuncType
                FROM ShiftLog AS s
                LEFT JOIN JobFunctions AS f ON s.FunctionID = f.ID
                WHERE s.ID = %s""",
            (ID,),
        )
        row = cur.fetchone()

    if not row:
        logger.warning("No Shift with the ID %s", ID)
        return None

    logger.debug("Returned Query: %s", row)

    return ShiftLogRow(
        id=row["ID"],
        zNumber=row["ZNumber"],
        functionID=row["FunctionID"],
        timeStarted=row["TimeStarted"],
        timeFinished=row["TimeFinished"],
        shiftID=row["ShiftID"],
        isAbsent=bool(row["IsAbsent"]),
        funcName=row["FuncName"],
        funcType=row["FuncType"],
    )


def editShift(
    conn: mysql.connector.MySQLConnection,
    ID: int,
    shiftStart: datetime = None,
    shiftEnd: datetime = None,
    key: str = None,
    func: str = None,
    isAbsent: bool = None,
) -> bool:
    """
    This function edits a shift already in the database.

    Args:
        conn: mySQL connector object
        ID: ShiftLog Primary Key
        the following arguments are entered if and only if
        changes are to be made
            shiftStart: datetime object for start of shift
            endShift: datetime object for end of shift
            key: string with the ShiftID
            func: string with the name of the function performed
            isAbsent: boolean with whether or not the shift is an absence

    Returns:
        bool: True if the shift successfully edits, false if it does not.
    """

    updates = []
    params = []
    funcID = None

    if shiftStart:
        updates.append("TimeStarted = %s")
        params.append(shiftStart)
    if shiftEnd:
        updates.append("TimeFinished = %s")
        params.append(shiftEnd)
    if key:
        updates.append("ShiftID = %s")
        params.append(key)
    if func:
        funcID = getFunctionID(conn, func)
        updates.append("FunctionID = %s")
        params.append(funcID)
        if func in ("Accountable", "PTO", "UTO", "VLE/VNS", "FMLA", "Sick"):
            isAbsent = "1"
        else:
            isAbsent = "0"
    if isAbsent == "1" or isAbsent == "0":
        updates.append("IsAbsent = %s")
        params.append(isAbsent)

    if not updates:
        return False

    params.append(ID)

    query = f"""
    UPDATE ShiftLog
    SET {', '.join(updates)}
    WHERE ID = %s
    """

    # TODO: Wrap multi-statement changes in explicit transactions with rollback.
    logger.debug("SQL Query: %s", query)
    logger.debug("SQL Parameters: %s", params)

    with conn.cursor() as cur:
        cur.execute(query, params)
        conn.commit()
        logger.info(
            f"Shift id {ID} changed: \nStartTime: {shiftStart} \nEndTime: {shiftEnd} \nKey: {key} \n Function: {funcID}-{func} \n isAbsent: {isAbsent}"
        )

    return True


def getJobs(conn: mysql.connector.MySQLConnection) -> dict[str, int]:
    """
    Fetch all job functions from the database and return them as a dictionary.

    Each key is a string in the format "Type - Name" and the value is the job's ID.

    Args:
        conn: A MySQL connection object.

    Returns:
        dict[str, int]: Dictionary where the key is the combined "Type - Name"
        of the job function, and the value is the corresponding job ID.
    """

    with conn.cursor() as cur:
        cur.execute(
            """
                SELECT ID, Name, Type
                FROM JobFunctions
                ORDER BY Type DESC, Name
            """
        )
        jobsRaw = cur.fetchall()

    jobs = {}

    for jobID, name, type in jobsRaw:
        label = f"{type} - {name}"
        jobs[label] = jobID

    logger.debug("jobs: %s", jobs)

    return jobs


def getShifts(conn: mysql.connector.MySQLConnection) -> list[str]:
    """
    Fetch all shift IDs from the database and return them as a sorted list.

    Args:
        conn: A MySQL connection object.

    Returns:
        list[str]: A list of all shift IDs in ascending order.
    """

    with conn.cursor() as cur:
        cur.execute(
            """
                    SELECT ID FROM Shifts
                    """
        )
        shiftsRaw = cur.fetchall()

    shifts = []

    for row in shiftsRaw:
        shifts.append(row[0])
    shifts.sort()
    logger.debug("shifts: %s", shifts)

    return shifts


def getFunctionID(conn: mysql.connector.MySQLConnection, function: str) -> int | None:
    """
    Retrieve the ID of a job function given its name.

    Args:
        conn: mySQL connector object
        function: string with the function Name

    Return:
        functionID: int with the primary key of the Function ID
        returns None if not found.
    """

    logger.debug("%s passed to getFunctionID.", function)

    with conn.cursor() as cur:
        cur.execute(
            """
                    SELECT ID 
                    FROM JobFunctions
                    WHERE Name = %s
                    """,
            (function,),
        )
        row = cur.fetchone()
    logger.debug("%s has ID of %s", function, row)
    return row[0] if row else None


def logShift(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    timeStart: datetime,
    timeEnd: datetime,
    key: str,
    function: str,
):
    """
    Logs a shift into the database.

    Args:
        conn: MySQL connector Object
        zNumber: string with the users zNumber
        timeStart: datetime with the shift Start
        timeEnd: datetime with the shift End
        key: string with the ShiftID
        function: string with the Function Name

    Returns:
        Nothing

    Notes:
        If a shift with the same parameters already exists, it will be skipped.
        Absence is automatically set for certain function types:
            Accountable, PTO, UTO, VLE/VNS, FMLA, Sick
    """

    functionID = getFunctionID(conn, function)

    absent = (
        1 if function in ("Accountable", "PTO", "UTO", "VLE/VNS", "FMLA", "Sick") else 0
    )

    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                    INSERT INTO ShiftLog (ZNumber, FunctionID, TimeStarted, TimeFinished, ShiftID, IsAbsent)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                (zNumber, functionID, timeStart, timeEnd, key, absent),
            )
            logger.info(
                "Shift logged from %s to %s as %s", timeStart, timeEnd, function
            )
            conn.commit()
        except mysql.connector.IntegrityError:
            logger.warning("Shift already exists! Insert skipped.")
        except Error as e:
            logger.error("Error!  %s", e)
    return


def getShiftsByDate(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    shiftIDs: list[str],
    absent: bool = False,
    startDate: datetime | None = None,
    endDate: datetime | None = None,
) -> tuple[str, tuple[str, str], list[ShiftByDateRow]]:
    """
    Retrieves shifts for a specific user, filtered by date, shift type, and absence.

    Args:
        conn: mySQL connector object.
        zNumber: string with the users zNumber
        home: boolean with whether the "home shift" is selected
        overtime: boolean with whether the "overtime shift" is selected
        absent: boolean with whether the "absence" is selected
        startDate: date with a start time to retrieve shifts
        endDate: date with a end time to retrieve shifts

    Returns:
        name: String with the user's name.
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    logger.debug("Passed start and end times for search: %s, %s", startDate, endDate)
    if startDate is None or endDate is None:
        raise ValueError("startDate and endDate must be provided as datetimes")
    whereClause, shiftTypes = _shift_id_clause(shiftIDs)

    query = f"""
    SELECT 
        s.ShiftID AS 'Key',
        s.TimeStarted,
        s.TimeFinished,
        e.FirstName,
        e.LastName,
        f.Name AS FuncName
    FROM ShiftLog AS s
    INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
    INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
    WHERE s.TimeStarted BETWEEN %s AND %s
    AND s.ZNumber = %s
    AND (
        (
            IsAbsent = 0
            {whereClause}
        )
        OR
        (
            %s = 1
            AND IsAbsent = 1
        )
    )
    ORDER BY s.TimeStarted DESC
    """

    params = [startDate, endDate, zNumber] + shiftTypes + [int(absent)]
    logger.debug("SQL Query resolved to: %s", query)
    logger.debug("SQL parameters resolved to: %s", params)

    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params)
        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    headers = [
        ("key", "Key"),
        ("weekday", "Day"),
        ("startTime", "Start Time"),
        ("endTime", "End Time"),
        ("function", "Function"),
        ("hours", "Time in Function"),
    ]

    name = "NULL"
    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"

    data = []
    for row in rawData:
        function_time = timeDifference(row["TimeStarted"], row["TimeFinished"])

        weekday = row["TimeStarted"].strftime("%A")

        data.append(
            ShiftByDateRow(
                key=row["Key"],
                weekday=weekday,
                startTime=row["TimeStarted"],
                endTime=row["TimeFinished"],
                function=row["FuncName"],
                hours=function_time,
            )
        )

    logger.debug("Data Returned from Query for %s", name)
    logger.debug("Headers: %s", headers)

    for row in data:
        logger.debug(
            "%s | %s | %s → %s | %s | %s hrs",
            row.key,
            row.weekday,
            row.startTime.strftime("%Y-%m-%d %H:%M"),
            row.endTime.strftime("%Y-%m-%d %H:%M"),
            row.function,
            row.hours,
        )

    return name, headers, data


def getShiftsByFunction(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    shiftIDs: list[str],
) -> tuple[str, tuple[tuple[str, str], ...], list[ShiftByFunction]]:
    """
    Retrieves and calculates how much time is spent in each function and returns
    formatted data for the Treeview.

    Args:
        conn: mySQL connector object
        zNumber: string of the users zNumber
        shiftIDs: list of ShiftID values to include in the report

    Returns:
        name: string containing the users name
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    whereClause, shiftTypes = _shift_id_clause(shiftIDs)

    query = f"""SELECT 
        f.Name AS FuncName,
        ROUND(
            SUM(TIMESTAMPDIFF(MINUTE, s.TimeStarted, s.TimeFinished)) / 60, 2
            ) 
            AS TotalHours,
        e.FirstName,
        e.LastName
    FROM ShiftLog AS s
    INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
    INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
    WHERE (IsAbsent = 0 {whereClause})
    AND s.ZNumber = %s
    GROUP BY e.ZNumber, e.FirstName, e.LastName, f.Name
	ORDER BY TotalHours DESC, f.Name;
    """

    params = shiftTypes + [zNumber]
    logger.debug("SQL Query resolved to: %s", query)
    logger.debug("SQL parameters resolved to: %s", params)

    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params)
        rawData = cur.fetchall()
    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    name = "NULL"
    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"
    totalTime = 0
    data = []
    for row in rawData:
        data.append(ShiftByFunction(funcName=row["FuncName"], hours=row["TotalHours"]))
        totalTime += row["TotalHours"]
    for item in data:
        item.percent = round(item.hours / totalTime * 100, 2)

    headers = [
        ("funcName", "Function"),
        ("hours", "Time In Function"),
        ("percent", "Percent Time in Function"),
    ]

    logger.debug("Data Returned from Query for %s", name)
    logger.debug("Headers: %s", headers)

    for item in data:
        logger.debug("%s | %s hrs | %s", item.funcName, item.hours, item.percent)

    return name, headers, data


def getShiftsByEquipment(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    shiftIDs: list[str],
) -> tuple[str, list[tuple[str, str]], list[ShiftByEquipment]]:
    """
    Retrieves and calculates how much time is spent on each equipment and returns
    formatted data for the Treeview.

    Args:
        conn: mySQL connector object
        zNumber: string of the users zNumber
        shiftIDs: list of ShiftID values to include in the report

    Returns:
        name: string containing the users name
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    whereClause, shiftTypes = _shift_id_clause(shiftIDs)

    query = f"""SELECT 
        eq.Name as EquipName,
        ROUND(
            SUM(TIMESTAMPDIFF(MINUTE, s.TimeStarted, s.TimeFinished)) / 60, 2
            ) 
            AS TotalHours,
        e.FirstName,
        e.LastName
    FROM ShiftLog AS s
    INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
    INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
    INNER JOIN Equipment AS eq ON f.Equipment = eq.ID
    WHERE (IsAbsent = 0 {whereClause})
    AND s.ZNumber = %s
    GROUP BY e.ZNumber, e.FirstName, e.LastName, f.Equipment
	ORDER BY TotalHours DESC, f.Equipment;
    """

    params = shiftTypes + [zNumber]
    logger.debug("SQL Query resolved to: %s", query)
    logger.debug("SQL parameters resolved to: %s", params)

    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params)
        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    name = "NULL"
    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"
    totalTime = 0
    data = []
    for row in rawData:
        data.append(
            ShiftByEquipment(equipName=row["EquipName"], hours=row["TotalHours"])
        )
        totalTime += row["TotalHours"]
    for item in data:
        percentCalculation = round(item.hours / totalTime * 100)
        item.percent = percentCalculation

    headers = [
        ("equipName", "Equipment"),
        ("hours", "Time On Equipment"),
        ("percent", "Percent Time in Equipment"),
    ]

    logger.debug("Data Returned from Query for %s", name)
    logger.debug("Headers: %s", headers)

    for item in data:
        logger.debug("%s | %s hrs | %s", item.equipName, item.hours, item.percent)

    return name, headers, data


def deleteShift(conn: mysql.connector.MySQLConnection, ID: int) -> None:
    """
    Deletes a row from the ShiftLog

    Args:
        conn: MySQL Connector Object
        ID: Shift Log Primary Key ID

    Returns:
        None: Logs a warning if the Shift ID doesn't exist.
    """

    row = getShiftLogRow(conn, ID)
    if row:
        startTime = row["TimeStarted"]
        endTime = row["TimeFinished"]
        funcName = row["FuncName"]
        with conn.cursor() as cur:
            cur.execute(
                """DELETE FROM ShiftLog
                    WHERE ID = %s
                    """,
                (ID,),
            )
            conn.commit()
        logger.info(
            "Shift from %s to %s as %s has been deleted.", startTime, endTime, funcName
        )
    else:
        logger.warning("Shift ID %s does not exist", ID)


def getMissedShifts(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    startDate: datetime | None = None,
    endDate: datetime | None = None,
) -> tuple[str, list[tuple[str, str]], list[AbsentShifts]]:
    """
    Retrieves a list of all shifts logged as absences.

    Args:
        conn: mySQL connector object
        zNumber: string of the users zNumber
        startDate: date object of a date to begin the search from
        endDate: date object of a date to conduct the search through

    Returns:
        name: string containing the users name
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    if startDate is None or endDate is None:
        raise ValueError("startDate and endDate must be provided as datetimes")

    with conn.cursor(dictionary=True) as cur:
        cur.execute(
            """SELECT 
            s.ShiftID,
            s.TimeStarted,
            s.TimeFinished,
            e.FirstName,
            e.LastName,
            f.Name AS 'FuncName'
        FROM ShiftLog AS s
        INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
        INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
        WHERE s.TimeStarted BETWEEN %s AND %s
        AND IsAbsent = 1
        AND s.ZNumber = %s
        ORDER BY  s.TimeStarted DESC
        """,
            (startDate, endDate, zNumber),
        )

        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    headers = [
        ("key", "Key"),
        ("day", "Day"),
        ("startTime", "Start Time"),
        ("endTime", "End Time"),
        ("absenceType", "Type of Absence"),
        ("duration", "Duration of Absence"),
    ]

    name = "NULL"
    data = []

    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"
        for row in rawData:  # Fills each row of the Dataclass.
            # Calculates the time in the function
            functionTime = timeDifference(row["TimeStarted"], row["TimeFinished"])

            # Figures what day of the week the row is and inserts in in front of the date.
            dateWorked = row["TimeStarted"]
            weekday = dateWorked.strftime("%A")

            data.append(
                AbsentShifts(
                    key=row["ShiftID"],
                    day=weekday,
                    startTime=row["TimeStarted"],
                    endTime=row["TimeFinished"],
                    absenceType=row["FuncName"],
                    duration=functionTime,
                )
            )

    logger.debug("Data Returned from Query for %s", name)
    logger.debug("Headers: %s", headers)

    for item in data:
        logger.debug(
            "%s | %s | %s → %s | %s | %s hrs",
            item.key,
            item.day,
            item.startTime,
            item.endTime,
            item.absenceType,
            item.duration,
        )

    return name, headers, data


def getAccountableShifts(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    startDate: datetime | None = None,
    endDate: datetime | None = None,
) -> tuple[str, list[str], list[list]]:
    """
    Retrieves a list of all shifts logged as absences.

    Args:
        conn: mySQL connector object
        zNumber: string of the users zNumber
        startDate: date object of a date to begin the search from
        endDate: date object of a date to conduct the search through

    Returns:
        name: string containing the users name
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    if startDate is None or endDate is None:
        raise ValueError("startDate and endDate must be provided as datetimes")

    with conn.cursor(dictionary=True) as cur:
        cur.execute(
            """SELECT 
            s.ShiftID,
            s.TimeStarted,
            s.TimeFinished,
            e.FirstName,
            e.LastName,
            f.Name AS 'FuncName'
        FROM ShiftLog AS s
        INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
        INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
        WHERE s.TimeStarted BETWEEN %s AND %s
        AND IsAbsent = 1
        AND f.Name = %s
        AND s.ZNumber = %s
        ORDER BY  s.TimeStarted DESC
        """,
            (startDate, endDate, "Accountable", zNumber),
        )

        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    headers = [
        ("key", "Key"),
        ("day", "Day"),
        ("startTime", "Start Time"),
        ("endTime", "End Time"),
        ("absenceType", "Type of Absence"),
        ("duration", "Duration of Absence"),
    ]

    name = "NULL"
    data = []

    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"
        for row in rawData:  # Fills each row of the Dataclass.
            # Calculates the time in the function
            functionTime = timeDifference(row["TimeStarted"], row["TimeFinished"])

            # Figures what day of the week the row is and inserts in in front of the date.
            dateWorked = row["TimeStarted"]
            weekday = dateWorked.strftime("%A")

            data.append(
                AbsentShifts(
                    key=row["ShiftID"],
                    day=weekday,
                    startTime=row["TimeStarted"],
                    endTime=row["TimeFinished"],
                    absenceType=row["FuncName"],
                    duration=functionTime,
                )
            )

    logger.debug("Data Returned from Query for %s", name)
    logger.debug("Headers: %s", headers)

    for item in data:
        logger.debug(
            "%s | %s | %s → %s | %s | %s hrs",
            item.key,
            item.day,
            item.startTime,
            item.endTime,
            item.absenceType,
            item.duration,
        )

    return name, headers, data


def timeSinceFunction(
    conn: mysql.connector.MySQLConnection,
    zNumber: str,
    shiftIDs: list[str],
) -> tuple[str, list[tuple[str, str]], list[TimeSince]]:
    """
    Retrieves and calculates how much time it has been
    since the last time each function was performed.

    Args:
        conn: mySQL connector object
        zNumber: string of the users zNumber
        shiftIDs: list of ShiftID values to include in the report

    Returns:
        name: string containing the users name
        headers: list[tuple(dataclass key, Header Label)] of the headers for the treeview.
        data: list[dataclass] of the data for the treeview.
    """

    whereClause, shiftTypes = _shift_id_clause(shiftIDs)

    query = f"""SELECT
        f.Name AS FuncName,
        MAX(s.TimeStarted) AS LastPerformed,
        e.FirstName,
        e.LastName
    FROM ShiftLog as s
    JOIN Employee AS e ON s.ZNumber = e.ZNumber
    JOIN JobFunctions AS f ON s.FunctionID = f.ID
    WHERE s.zNumber = %s AND s.IsAbsent = 0 {whereClause}
    GROUP BY f.ID, f.Name
    ORDER BY LastPerformed DESC;
    """
    params = [zNumber] + shiftTypes

    logger.debug("SQL Query Resolved as: %s", query)
    logger.debug("SQL Query Parameters as: %s", params)

    with conn.cursor(dictionary=True) as cur:
        cur.execute(query, params)
        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    headers = [
        ("funcName", "Function"),
        ("funcDate", "Date"),
        ("daysSince", "Days Since"),
    ]

    name = "NULL"
    data = []
    if rawData:
        name = f"{rawData[0]['LastName']}, {rawData[0]['FirstName']}"
        for row in rawData:
            shiftDate = row[
                "LastPerformed"
            ].date()  # Remove the time from the shiftStart time.
            daysDelta = (
                date.today() - shiftDate
            ).days  # Figures the delta since this shift.
            data.append(
                TimeSince(
                    funcName=row["FuncName"], funcDate=shiftDate, daysSince=daysDelta
                )
            )

    for item in data:
        logger.debug(
            "%s | %s | %s",
            item.funcName,
            item.funcDate.strftime("%Y-%m-%d"),
            item.daysSince,
        )

    return name, headers, data


def printShiftLogTable(conn: mysql.connector.MySQLConnection) -> None:
    """
    This prints the shiftlog to the terminal in a readable format.
    Used for debugging purposes

    Args:
        conn: MySQL connector Object

    Returns:
        None: Prints to the terminal the entire shiftLog for debugging.
    """

    with conn.cursor(dictionary=True) as cur:
        cur.execute(
            """SELECT 
                    s.ShiftID, 
                    s.TimeStarted, 
                    s.TimeFinished, 
                    e.FirstName, 
                    e.LastName, 
                    f.Name AS 'FuncName'
                    FROM ShiftLog as s
                    INNER JOIN Employee AS e ON s.ZNumber = e.ZNumber
                    INNER JOIN JobFunctions AS f ON s.FunctionID = f.ID
                    ORDER BY s.TimeStarted DESC
                    """
        )
        rawData = cur.fetchall()

    for row in rawData:
        logger.debug(" | ".join(str(value) for value in row.values()))

    data = []

    for row in rawData:  # Reformat each row for the correct data
        functionTime = timeDifference(
            row["TimeStarted"], row["TimeFinished"]
        )  # Calculates the time in the function

        # Figures what day of the week the row is and inserts in in front of the date.
        weekday = row["TimeStarted"].strftime("%A")

        data.append(
            [
                row["ShiftID"],
                weekday,
                row["TimeStarted"],
                row["TimeFinished"],
                row["FirstName"],
                row["LastName"],
                row["FuncName"],
                functionTime,
            ]
        )

    headers = [
        "Key",
        "Day",
        "Start Time",
        "End Time",
        "First Name",
        "Last Name",
        "Function",
        "Time in Function",
    ]

    # The rest of this formats the output for aligned columns for Terminal
    strData = [[("" if col is None else str(col)) for col in row] for row in data]

    colWidth = []
    for colIDX in range(len(headers)):
        longest = len(headers[colIDX])
        for row in strData:
            longest = max(longest, len(row[colIDX]))
        colWidth.append(longest)

    formatString = " | ".join("{:<" + str(width) + "}" for width in colWidth)

    print(formatString.format(*headers))

    separatorLength = sum(colWidth) + (3 * (len(headers) - 1))
    print("-" * separatorLength)

    if not data:
        print("(No Data to Display)")

    for row in strData:
        print(formatString.format(*row))


if __name__ == "__main__":
    configureLogging()
    conn, user = getConn()
    if conn:
        # getJobs(conn)
        printShiftLogTable(conn)
        # getShiftsByDate(conn, user, True, True, True, True)
        # getShiftsByFunction(conn, user, True, True, True, True)
        # timeSinceFunction(conn, user, True, True)
