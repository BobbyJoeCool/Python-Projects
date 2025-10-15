'''
Majors table
MajorID: INTEGER PRIMARY KEY
Name: Text

Departments table
DeptID INTEGER PRIMARY KEY
Name TEXT

Students table
StudentID: INTEGER PRIMARY KEY
Name: TEXT
MajorID: INTEGER Foreign Key
DeptID: INTEGER Foreign Key
'''

import sqlite3
import random

def get_connection():
    """Return a connection and cursor to the database."""
    db = sqlite3.connect("school.db")
    cur = db.cursor()
    return db, cur

### Create a the table
def create_tables():
    # Create the Major Table
    db, cur = get_connection()

    # Drop the Tables (in reverse dependency order)
    cur.execute("DROP TABLE IF EXISTS Students")
    cur.execute("DROP TABLE IF EXISTS Majors")
    cur.execute("DROP TABLE IF EXISTS Departments")

    cur.execute(
        """CREATE TABLE IF NOT EXISTS Majors(
        MajorID INTEGER PRIMARY KEY NOT NULL,
        Name TEXT
        )"""
    )

    # Create the Department Table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS Departments(
        DeptID INTEGER PRIMARY KEY NOT NULL,
        Name TEXT
        )"""
    )

    # Create the Students Table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS Students(
            StudentID INTEGER PRIMARY KEY NOT NULL,
            Name TEXT,
            MajorID INTEGER,
            DeptID INTEGER,
            FOREIGN KEY (MajorID) REFERENCES Majors(MajorID),
            FOREIGN KEY (DeptID) REFERENCES Departments(DeptID)
        )"""
    )
    # Commits these tables.
    db.commit()
    db.close()

### Auto Populate the Table
def populate_data():
    # Example department names
    db, cur = get_connection()
    departments = [
        "Math",
        "Computer Science",
        "Sciences",
        "Business",
        "Humanities",
        "English"
    ]

    # Insert Departments
    cur.executemany("INSERT INTO Departments(Name) VALUES (?)", [(d,) for d in departments])

    # Example major prefixes
    major_prefixes = [
        "Software Development", 
        "Political Science", 
        "Physics", 
        "Mathamatics", 
        "Education",
        "Literature", 
        "History", 
        "Philosophy", 
        "Linguistics", 
        "Psychology",
        "Biology", 
        "Chemistry", 
        "Sociology", 
        "Engineering", 
        "Astronomy",
        "Finance", 
        "Accounting", 
        "Marketing", 
        "Music", 
        "Nursing"
    ]

    # Insert Majors (each assigned to a random department)
    for major in major_prefixes:
        dept_id = random.randint(1, len(departments))
        cur.execute("INSERT INTO Majors(Name) VALUES (?)", (f"{major}",))

    # Example student name parts
    first_names = ["Alex", "Taylor", "Jordan", "Casey", "Morgan", "Riley", "Jamie", "Drew", "Skyler", "Peyton"]
    last_names = ["Smith", "Johnson", "Lee", "Brown", "Garcia", "Martinez", "Davis", "Lopez", "Wilson", "Anderson"]

    # Insert Students (each with a random major and department)
    for _ in range(15):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        major_id = random.randint(1, 20)
        # Look up which department that major belongs to
        dept_id = random.randint(1, len(departments))
        cur.execute(
            "INSERT INTO Students(Name, MajorID, DeptID) VALUES (?, ?, ?)",
            (name, major_id, dept_id)
        )

    db.commit()
    db.close()

### Funtions to return lists or id numbers
def get_departments():
    db, cur = get_connection()
    # Return a list of all department names.
    cur.execute("SELECT Name FROM Departments ORDER BY Name")
    depts = [row[0] for row in cur.fetchall()]
    db.close()
    return depts


def get_majors():
    db, cur = get_connection()
    # Return a list of all major names.
    cur.execute("SELECT Name FROM Majors ORDER BY Name")
    majrs = [row[0] for row in cur.fetchall()]
    db.close()
    return majrs


def get_students():
    db, cur = get_connection()
    # Return a list of all student names.
    cur.execute("SELECT Name FROM Students ORDER BY Name")
    stdnts = [row[0] for row in cur.fetchall()]
    db.close()
    return stdnts


def get_dept_id(dept_name):
    db, cur = get_connection()
    """Return the DeptID for a given department name."""
    cur.execute("SELECT DeptID FROM Departments WHERE Name = ?", (dept_name,))
    result = cur.fetchone()
    deptID = result[0] if result else None
    db.close()
    return deptID


def get_major_id(major_name):
    db, cur = get_connection()
    """Return the MajorID for a given major name."""
    cur.execute("SELECT MajorID FROM Majors WHERE Name = ?", (major_name,))
    result = cur.fetchone()
    majorID = result[0] if result else None
    db.close()
    return majorID


def get_student_id(student_name):
    db, cur = get_connection()
    """Return the StudentID for a given student name."""
    cur.execute("SELECT StudentID FROM Students WHERE Name = ?", (student_name,))
    result = cur.fetchone()
    studentID = result[0] if result else None
    db.close()
    return studentID


### Major Table Functions
def add_major(name):
    """Add a new major. Returns True if successful, False if major exists."""
    db, cur = get_connection()
    # Check if major already exists
    cur.execute("SELECT MajorID FROM Majors WHERE Name = ?", (name,))
    if cur.fetchone():
        db.close()
        return False  # Major already exists
    # Insert new major
    cur.execute("INSERT INTO Majors (Name) VALUES (?)", (name,))
    db.commit()
    db.close()
    return True

def search_major(name):
    """Search for a major by name. Returns major ID if found, else None."""
    db, cur = get_connection()
    cur.execute("SELECT MajorID FROM Majors WHERE Name = ?", (name,))
    result = cur.fetchone()
    majorid = result[0] if result else None
    db.close()
    return majorid

def update_major(old_name, new_name):
    """Update an existing major's name. Returns True if successful."""
    db, cur = get_connection()
    # Check that the old major exists
    cur.execute("SELECT MajorID FROM Majors WHERE Name = ?", (old_name,))
    if not cur.fetchone():
        db.close()
        return False  # Old major does not exist
    # Update major name
    cur.execute("UPDATE Majors SET Name = ? WHERE Name = ?", (new_name, old_name))
    db.commit()
    db.close()
    return True


def delete_major(name):
    """Delete a major by name. Returns True if successful, False if not found."""
    db, cur = get_connection()
    cur.execute("SELECT MajorID FROM Majors WHERE Name = ?", (name,))
    if not cur.fetchone():
        db.close()
        return False  # Major not found
    cur.execute("DELETE FROM Majors WHERE Name = ?", (name,))
    db.commit()
    db.close()
    return True


def list_majors():
    """Return a dictionary of majors with the key of MajorID and value of the Major Name."""
    db, cur = get_connection()
    cur.execute("SELECT Name, MajorID FROM Majors ORDER BY Name")
    majors = {row[1]: row[0] for row in cur.fetchall()}
    db.close()
    return majors


### Department Table Functions
def add_department(name):
    """Add a new department. Returns True if successful, False if it exists."""
    db, cur = get_connection()
    cur.execute("SELECT DeptID FROM Departments WHERE Name = ?", (name,))
    if cur.fetchone():
        db.close()
        return False  # Department already exists
    cur.execute("INSERT INTO Departments (Name) VALUES (?)", (name,))
    db.commit()
    db.close()
    return True


def search_department(name):
    """Search for a department by name. Returns DeptID if found, else None."""
    db, cur = get_connection()
    cur.execute("SELECT DeptID FROM Departments WHERE Name = ?", (name,))
    result = cur.fetchone()
    depts = result[0] if result else None
    db.close()
    return depts


def update_department(old_name, new_name):
    """Update an existing department's name. Returns True if successful."""
    db, cur = get_connection()
    cur.execute("SELECT DeptID FROM Departments WHERE Name = ?", (old_name,))
    if not cur.fetchone():
        db.close()
        return False  # Department does not exist
    cur.execute("UPDATE Departments SET Name = ? WHERE Name = ?", (new_name, old_name))
    db.commit()
    db.close()
    return True


def delete_department(name):
    """Delete a department by name. Returns True if successful, False if not found."""
    db, cur = get_connection()
    cur.execute("SELECT DeptID FROM Departments WHERE Name = ?", (name,))
    if not cur.fetchone():
        db.close()
        return False  # Department not found
    cur.execute("DELETE FROM Departments WHERE Name = ?", (name,))
    db.commit()
    db.close()
    return True


def list_departments():
    """Return a dictionary of all department names and IDs."""
    db, cur = get_connection()
    cur.execute("SELECT Name, DeptID FROM Departments ORDER BY Name")
    departments = {row[1]: row[0] for row in cur.fetchall()}
    db.close()
    return departments


### Student Table Functions
def add_student(name, major_id, dept_id):
    """
    Add a new student. Returns True if successful, False if student already exists.
    name: string
    major_id: int
    dept_id: int
    """
    db, cur = get_connection()
    # Check if student already exists (by name)
    cur.execute("SELECT StudentID FROM Students WHERE Name = ?", (name,))
    if cur.fetchone():
        db.close()
        return False
    cur.execute("INSERT INTO Students (Name, MajorID, DeptID) VALUES (?, ?, ?)", 
                (name, major_id, dept_id))
    db.commit()
    db.close()
    return True


def search_student(name):
    """Search for a student by name. Returns a tuple (StudentID, MajorName, DeptName) if found, else None."""
    db, cur = get_connection()
    
    cur.execute("""
        SELECT s.StudentID, m.Name AS MajorName, d.Name AS DeptName
        FROM Students s
        LEFT JOIN Majors m ON s.MajorID = m.MajorID
        LEFT JOIN Departments d ON s.DeptID = d.DeptID
        WHERE s.Name = ?
    """, (name,))
    
    result = cur.fetchone()
    db.close()
    
    if result:
        return {
            "StudentID": result[0],
            "Major": result[1] if result[1] else "N/A",
            "Department": result[2] if result[2] else "N/A"
        }
    else:
        return None


def update_student(student_id, new_name=None, new_major_id=None, new_dept_id=None):
    """
    Update an existing student's information.
    Only non-None fields will be updated.
    Returns True if successful, False if student not found.
    """
    db, cur = get_connection()
    cur.execute("SELECT * FROM Students WHERE StudentID = ?", (student_id,))
    if not cur.fetchone():
        db.close()
        return False  # Student not found

    # Build the update dynamically based on non-None parameters
    fields = []
    values = []

    if new_name is not None:
        fields.append("Name = ?")
        values.append(new_name)
    if new_major_id is not None:
        fields.append("MajorID = ?")
        values.append(new_major_id)
    if new_dept_id is not None:
        fields.append("DeptID = ?")
        values.append(new_dept_id)

    if fields:
        sql = f"UPDATE Students SET {', '.join(fields)} WHERE StudentID = ?"
        values.append(student_id)
        cur.execute(sql, tuple(values))
        db.commit()

    db.close()
    return True


def delete_student(student_id):
    """Delete a student by StudentID. Returns True if successful, False if not found."""
    db, cur = get_connection()
    cur.execute("SELECT StudentID FROM Students WHERE StudentID = ?", (student_id,))
    if not cur.fetchone():
        db.close()
        return False  # Student not found
    cur.execute("DELETE FROM Students WHERE StudentID = ?", (student_id,))
    db.commit()
    db.close()
    return True


def list_students():
    """
    Return a list of all students with their information:
    Student ID, Name, Major Name, Department Name
    """
    db, cur = get_connection()
    cur.execute("""
        SELECT s.StudentID, s.Name, m.Name, d.Name
        FROM Students s
        LEFT JOIN Majors m ON s.MajorID = m.MajorID
        LEFT JOIN Departments d ON s.DeptID = d.DeptID
        ORDER BY s.Name
    """)
    stdnts = cur.fetchall()  # List of tuples: (StudentID, Name, Major, Department)
    db.close()
    return stdnts