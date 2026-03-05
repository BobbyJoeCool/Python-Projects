# This contains all the helper functions that turn the database data into useable information for the user.

import logging
import os
from datetime import timedelta


def configureLogging():
    # Gets the directory the main.py is in, and creates a Log directory if it doesn't exist
    BASEDIR = os.path.dirname(os.path.abspath(__file__))
    LOGDIR = os.path.join(BASEDIR, "Logs")
    os.makedirs(LOGDIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # Operational Log
    opLog = logging.FileHandler(os.path.join(LOGDIR, "op.log"), encoding="utf-8")
    opLog.setLevel(logging.INFO)
    opLog.setFormatter(formatter)

    # Debug Log
    debugLog = logging.FileHandler(os.path.join(LOGDIR, "debug.log"), encoding="utf-8")
    debugLog.setLevel(logging.DEBUG)
    debugLog.setFormatter(formatter)

    consoleLog = logging.StreamHandler()
    consoleLog.setLevel(logging.INFO)
    consoleLog.setFormatter(formatter)

    logger.addHandler(opLog)
    logger.addHandler(debugLog)
    logger.addHandler(consoleLog)


def timeDifference(start, end):
    # TODO: Add unit tests for timeDifference() boundary cases (overnight shifts).
    if end < start:
        end += timedelta(days=1)
    jobTime = (end - start).total_seconds() / 3600
    return jobTime
