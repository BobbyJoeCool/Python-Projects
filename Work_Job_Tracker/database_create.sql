-- Creates the database for the Work_Job_Tracker App.

DROP DATABASE IF EXISTS workJobTrackerDB;
CREATE DATABASE workJobTrackerDB;

USE workJobTrackerDB;

-- Create a User for the Python Scripts and .env file.
DROP USER IF EXISTS 'z002p25'@'localhost';
CREATE USER 'z002p25'@'localhost' IDENTIFIED BY 'password12345';
GRANT ALL PRIVILEGES ON workJobTrackerDB.* TO 'z002p25'@'localhost';
FLUSH PRIVILEGES;

-- =============
-- Create Tables

CREATE TABLE JobFunctions (
    FunctionID INT PRIMARY KEY AUTO_INCREMENT,
    FunctionName VARCHAR(50),
    FunctionType VARCHAR(50),
    Equipment VARCHAR(2),
    ProdFunction BOOL
);

CREATE TABLE Shifts (
    ShiftID VARCHAR(2) PRIMARY KEY,
    ShiftDays VARCHAR(100),
    ShiftTimes VARCHAR(100)
);

CREATE TABLE Employee (
    ZNumber VARCHAR(7) PRIMARY KEY,
    FirstName VARCHAR(30),
    LastName VARCHAR(50),
    HomeShift VARCHAR(2),
    FOREIGN KEY (HomeShift) REFERENCES Shifts(ShiftID)
);

CREATE TABLE ShiftLog (
    ShiftLogID INT PRIMARY KEY AUTO_INCREMENT,
    ZNumber VARCHAR(7),
    FunctionID INT,
    DateWorked DATE,
    TimeStarted TIME,
    TimeFinished TIME,
    ShiftID VARCHAR(2),
    FOREIGN KEY (ZNumber) REFERENCES Employee(ZNumber),
    FOREIGN KEY (FunctionID) REFERENCES JobFunctions(FunctionID),
    FOREIGN KEY (ShiftID) REFERENCES Shifts(ShiftID)
);

INSERT INTO Shifts (ShiftID, ShiftDays, ShiftTimes)
VALUES
    ("B1", "Tuesday-Friday", "6:00 AM - 4:00 PM"),
    ("B2", "Tuesday-Friday", "4:00 PM - 2:00 AM"),
    ("A1", "Saturday-Monday", "6:00 AM - 6:00 PM"),
    ("A2", "Saturday-Monday", "6:00 PM - 6:00 AM");

INSERT INTO Employee (ZNumber, FirstName, LastName, HomeShift)
VALUES
    ('Z002P25', 'Robert', 'Breutzmann', "B1");

INSERT INTO JobFunctions (FunctionName, FunctionType, Equipment, ProdFunction)
VALUES
    ('Bulk', 'Pull', 'RC', 1),
    ('Full Pallet', 'Pull', 'RR', 1),
    ('Rack Puts', 'Put', 'RR', 1),
    ('GPM', 'GPM', 'PR', 0),
    ('Tugger', 'GPM', 'TR', 0),
    ('Carton Air', 'Pull', 'SP', 1),
    ('Carton Floor', 'Pull', 'TR', 1),
    ('Non-Con Carton Air', 'Pull', 'SP', 1),
    ('OS Puts', 'Put', 'SP', 1),
    ('Rack Consolidation', 'IM', 'RR', 0),
    ('Bulk Consolidation', 'IM', 'RC', 0),
    ('XS Consolidation', 'IM', 'SP', 0),
    ('Carton Air Captain', 'IM', 'SP', 0),
    ('Projects', 'IM', NULL, 0),
    ('Light Duty', 'Other', NULL, 0);