# contains all the database functions

import mysql.connector
from mysql.connector import Error
from dotenv import dotenv_values
import os

def getConn():
    baseDir = os.path.dirname(os.path.abspath(__file__))
    envPath = os.path.join(baseDir, "setup.env")
    setup = dotenv_values(envPath)

    config = {
        "host": setup["DB_HOST"],
        "user": setup["DB_USER"],
        "password": setup["DB_PASSWORD"],
        "database": setup["DB_NAME"],
        "raise_on_warnings": True 
    }

    try:
        conn = mysql.connector.connect(**config)
        if not conn.is_connected():
            print("Could not connect to database.")
            return None
        return conn

    except Error as e:
        print("Error: ", e)
        return None
    
def getJobs(): # Placeholder until DB function is complete
    jobs = ["Bulk",
            "Full Pallet",
            "Rack Puts",
            "GPM",
            "Tugger",
            "Carton Air",
            "Carton Floor",
            "Non-Con Carton Air",
            "OS Puts",
            "Rack Consolidation",
            "Bulk Consolidation",
            "XS Consolidation",
            "Carton Air Captain",
            "Projects",
            "Light Duty"]
    jobs.sort()
    return jobs

def getShifts(): # Placeholder until DB function is complete
    shifts = ["A1", "B1", "A2", "B2"]
    shifts.sort()
    return shifts