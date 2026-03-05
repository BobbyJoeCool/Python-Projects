"""Domain models for the Work Job Tracker application.

This module defines dataclasses that represent business-domain records and
query results. These classes are shared across layers.

The models in this file intentionally avoid any dependence on:
- Tkinter widgets or GUI-specific concerns
- MySQL connector objects

They are suitable for type checking, unit tests, and UI display.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ShiftByDateRow:
    """Row model for the "Shifts by Date" report."""

    key: str
    weekday: str
    startTime: datetime
    endTime: datetime
    function: str
    hours: float


@dataclass(slots=True)
class ShiftLogRow:
    """Row model for a ShiftLog record with joined function metadata."""

    id: int
    zNumber: str
    functionID: int
    timeStarted: datetime
    timeFinished: datetime
    shiftID: str
    isAbsent: bool
    funcName: str
    funcType: str


@dataclass(slots=True)
class ShiftByFunction:
    """Row model for the "Shifts by Function" summary report."""

    funcName: str
    hours: float
    percent: float = 0.0


@dataclass(slots=True)
class ShiftByEquipment:
    """Row model for the "Shifts by Equipment" summary report."""

    equipName: str
    hours: float
    percent: float = 0.0


@dataclass(slots=True)
class AbsentShifts:
    """Row model for the "Absent Shifts" report."""

    key: str
    day: str
    startTime: datetime
    endTime: datetime
    absenceType: str
    duration: float


@dataclass(slots=True)
class TimeSince:
    """Row model for the "Time Since Function" report."""

    funcName: str
    funcDate: datetime
    daysSince: int
