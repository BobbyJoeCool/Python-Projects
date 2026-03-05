-- Creates the database for the Work_Job_Tracker App.

DROP DATABASE IF EXISTS workJobTrackerDB;
CREATE DATABASE workJobTrackerDB;

USE workJobTrackerDB;

-- Create a User for the Python Scripts and .env file.
DROP USER IF EXISTS 'z002p25'@'localhost';
CREATE USER 'z002p25'@'localhost' IDENTIFIED BY 'NukeUm85';
GRANT ALL PRIVILEGES ON workJobTrackerDB.* TO 'z002p25'@'localhost';



FLUSH PRIVILEGES;

-- =============
-- Create Tables

CREATE TABLE Equipment (
    ID VARCHAR(2) PRIMARY KEY,
    Name VARCHAR(75)
);

CREATE TABLE JobFunctions (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Type VARCHAR(50),
    Equipment VARCHAR(2),
    Prod BOOL,
    FOREIGN KEY (Equipment) REFERENCES Equipment(ID)
);

CREATE TABLE Shifts (
    ID VARCHAR(2) PRIMARY KEY,
    Days VARCHAR(100),
    Times VARCHAR(100)
);

CREATE TABLE Employee (
    ZNumber VARCHAR(7) PRIMARY KEY,
    PasswordHash VARCHAR(255),
    FirstName VARCHAR(30),
    LastName VARCHAR(50),
    HomeShift VARCHAR(2),
    Role VARCHAR(50),
    FOREIGN KEY (HomeShift) REFERENCES Shifts(ID)
);

CREATE TABLE ShiftLog (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    ZNumber VARCHAR(7),
    FunctionID INT,
    TimeStarted DATETIME,
    TimeFinished DATETIME,
    ShiftID VARCHAR(2),
    IsAbsent BOOL,
    FOREIGN KEY (ZNumber) REFERENCES Employee(ZNumber),
    FOREIGN KEY (FunctionID) REFERENCES JobFunctions(ID),
    FOREIGN KEY (ShiftID) REFERENCES Shifts(ID),
    UNIQUE KEY UniqueShift (ZNumber, TimeStarted, TimeFinished)
);

INSERT INTO Shifts (ID, Days, Times)
VALUES
    ("B1", "Tuesday-Friday", "6:00 AM - 4:00 PM"),
    ("B2", "Tuesday-Friday", "4:00 PM - 2:00 AM"),
    ("A1", "Saturday-Monday", "6:00 AM - 6:00 PM"),
    ("A2", "Saturday-Monday", "6:00 PM - 6:00 AM");

INSERT INTO Employee (ZNumber, FirstName, LastName, HomeShift, Role)
VALUES
    ('Z002P25', 'Robert', 'Breutzmann', 'B1', 'Admin'),
    ('Z002P00', 'Example', 'Admin', 'B1', 'Admin'),
    ('Z002P26', 'Example', 'Employee', 'B1', 'Worker'),
    ('Z002P24', 'Example', 'Manager', 'B1', 'Manager');
    
INSERT INTO Equipment (ID, Name)
VALUES
	('SP', 'Order Picker'),
    ('TR', 'Tugger'),
    ('RC', 'Forklift'),
    ('RR', 'Reach Truck'),
    ('PR', 'Pallet Rider');

INSERT INTO JobFunctions (Name, Type, Equipment, Prod)
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
    ('Light Duty', 'Other', NULL, 0),
    ('Training', 'Other', NULL, 0),
    ('Accountable', NULL, NULL, 0),
    ('PTO', NULL, NULL, 0),
    ('UTO', NULL, NULL, 0),
    ('VLE/VNS', NULL, NULL, 0),
    ('Sick', NULL, NULL, 0);