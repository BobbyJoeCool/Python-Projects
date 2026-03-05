import logging
import tkinter as tk
from datetime import date, datetime, time
from tkinter import messagebox, ttk

import logic
from tkcalendar import DateEntry

logger = logging.getLogger("gui.py")


class LoginScreen(tk.Toplevel):
    def submitLogin(self):
        try:
            conn, user = logic.authenticate(self.username.get(), self.password.get())
            self.result = (conn, user)
            self.destroy()
        except logic.InvalidLoginError as e:
            logger.warning("Login failed for user '%s': %s", self.username.get(), e)
            messagebox.showerror(
                "Login Failed", "Invalid Username/Password Combination."
            )
        except Exception as e:
            logger.exception(
                "Unexpected error during login for user '%s'", self.username.get(), e
            )
            messagebox.showerror("Error", "Unexpected error occurred.")

    def cancel(self):
        self.result = None
        self.destroy()

    def __init__(self, parent):
        super().__init__(parent)
        # TODO: Add role-aware login feedback (manager/admin) and allow admins to act on other users.
        self.geometry("200x200")
        self.title("Login")
        self.resizable(False, False)
        self.parent = parent
        self.result = None
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        loginLabel = ttk.Label(self, text="Enter you Login Information")
        loginLabel.pack(pady=(10, 20))

        loginUsernameFrame = ttk.Frame(self)
        loginUserLabel = ttk.Label(loginUsernameFrame, text="Username: ")
        loginUserEntry = ttk.Entry(loginUsernameFrame, textvariable=self.username)
        loginUsernameFrame.pack(pady=10)
        loginUserLabel.pack(side="left")
        loginUserEntry.pack(side="left")

        loginPasswordFrame = ttk.Frame(self)
        loginPasswordLabel = ttk.Label(loginPasswordFrame, text="Password: ")
        loginPasswordEntry = ttk.Entry(
            loginPasswordFrame, textvariable=self.password, show="*"
        )
        loginPasswordFrame.pack(pady=10)
        loginPasswordLabel.pack(side="left")
        loginPasswordEntry.pack(side="left")

        loginButtonFrame = ttk.Frame(self)
        loginButton = ttk.Button(
            loginButtonFrame, text="Login", command=self.submitLogin
        )
        exitButton = ttk.Button(loginButtonFrame, text="Exit", command=self.cancel)
        loginButtonFrame.pack(pady=10)
        loginButton.pack(side="left")
        exitButton.pack(side="left")


def dataclassesToRows(
    data: list[object],
    headers: list[tuple[str, str]],
    formatters: dict[str, callable] | None = None,
) -> tuple[list[list[object]], list[str]]:
    """
    Convert a list of dataclass instances into Treeview-compatible rows.

    Args:
        data: list of dataclass instances
        headers: list of the dataclass header dictionary.
        fieldOrder: ordered list of field names to extract
        formatters: optional mapping of field_name -> formatter function

    Returns:
        list[list] suitable for Treeview insertion
    """

    formatters = formatters or {}
    # TODO: Move report formatting into the logic layer to keep GUI thin/testable.

    fieldOrder = [field for field, _ in headers]
    columnHeaders = [label for _, label in headers]

    rows = []

    for obj in data:
        row = []
        for field in fieldOrder:
            value = getattr(obj, field)

            if field in formatters:
                value = formatters[field](value)

            row.append(value)
        rows.append(row)

    return rows, columnHeaders


def clearTreeview(tree: ttk.Treeview) -> None:
    """Clear all rows and columns from a Treeview.

    Args:
        tree: The ttk.Treeview to clear.

    Return:
        None
    """
    tree.delete(*tree.get_children())  # Clear the report view.
    tree["displaycolumns"] = ()  # removes all columns


def setupTreeview(
    tree: ttk.Treeview,
    header: list[str],
    data: list[list[object]],
    labelVar: tk.StringVar,
    label: str,
) -> None:
    """Configure a Treeview with new headers and insert row data.

    Args:
        tree: The ttk.Treeview to configure.
        header: List of column header strings.
        data: 2D list of row values to insert.
        labelVar: Tk StringVar to update with a table label.
        label: Label text to set.

    Return:
        None
    """
    # Configure new headers
    labelVar.set(label)
    tree["columns"] = header
    tree["displaycolumns"] = header
    tree["show"] = "headings"

    for col in header:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for row in data:
        tree.insert("", "end", values=row)


class GUI:
    def __init__(self, master, conn, user):
        # TODO: Add role-based navigation (show Manager/Admin tabs by user.role).
        self.master = master
        self.master.title("Work Job Tracker")
        self.master.geometry("1000x600")

        self.style = ttk.Style()
        self.style.theme_use("aqua")

        self.style.configure(
            "Quit.TButton", foreground="firebrick1", font=("Arial", 12, "bold")
        )
        self.style.configure(
            "Log.TButton", foreground="gold", font=("Arial", 12, "bold")
        )
        self.style.configure("Header.Label", font=("", 18, "bold"))

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)
        self.quitButton = ttk.Button(
            master, text="EXIT", command=master.destroy, style="Quit.TButton"
        )
        self.notebook.pack()
        self.quitButton.pack(side="bottom", pady=10)

        self.logPage = LogPage(self.notebook, conn, user)
        self.reportsPage = ReportsPage(self.notebook, conn, user)

        self.notebook.add(self.logPage, text="Log Shift")
        self.notebook.add(self.reportsPage, text="Reports")


class LogPage(ttk.Frame):
    def logShift(self) -> bool | None:
        """Validate and log a shift entry for the active user.

        Return:
            True if the shift was logged.
            False if the user cancelled or validation failed.
        """

        # TODO: Allow managers/admins to log shifts for other Z-numbers.
        startTime = self.shiftStart.getDateTime()
        endTime = self.shiftEnd.getDateTime()

        jobParts = self.selectedJob.get().split(" - ", 1)
        job = jobParts[1] if len(jobParts) > 1 else jobParts[0]

        jobTime, isZero, isLong = logic.evaluate_shift_duration(startTime, endTime)

        if isZero:
            messagebox.showerror("ERROR!", "The shift you entered is for 0 hours.")
            return False

        if isLong:
            isOK = messagebox.askokcancel(
                "WARNING!",
                f"The shift you entered is for {jobTime:.2f} hours, this is greater than 12 hours.  Do you wish to proceed?",
            )
            if isOK is False:
                return False

        confirmed = messagebox.askokcancel(
            "Confirm Entry",
            f"You entered {jobTime:.2f} hours of {job}.  Is this correct?",
        )
        if confirmed is False:
            return False

        key = self.selectedShift.get()
        logic.log_shift(self.conn, self.user, startTime, endTime, key, job)
        return True

    def __init__(self, parent, conn, user):
        super().__init__(parent)
        # TODO: Add method-level docstrings for GUI handlers and setup methods.
        self.pack_configure(fill="both", expand=True)
        self.conn = conn
        self.user = user

        # Job Function Selection and Key
        self.jobMap = logic.get_jobs(self.conn)
        self.jobs = list(self.jobMap.keys())
        self.selectedJob = tk.StringVar()

        self.jobSelectFrame = ttk.Frame(self)
        self.jobLabel = ttk.Label(self.jobSelectFrame, text="Select Job Function")
        self.jobSelection = ttk.Combobox(
            self.jobSelectFrame,
            textvariable=self.selectedJob,
            values=self.jobs,
            state="readonly",
        )
        self.jobLabel.pack(side="left")
        self.jobSelection.pack(side="left")

        self.shifts = logic.get_shifts(self.conn)
        self.selectedShift = tk.StringVar()
        self.selectedShift.set("B1")

        self.shiftKeyLabel = ttk.Label(self.jobSelectFrame, text="Enter Key:")
        self.shiftKeyComboBox = ttk.Combobox(
            self.jobSelectFrame,
            textvariable=self.selectedShift,
            values=self.shifts,
            state="readonly",
            width=3,
        )

        self.shiftKeyLabel.pack(side="left", padx=(10, 0))
        self.shiftKeyComboBox.pack(side="left")

        # Start / End Time
        self.timeSelectLabel = ttk.Label(
            self,
            text="Enter the Start and Finish Time of the job function",
            justify="center",
        )

        self.timeStartFrame = ttk.Frame(self)
        self.shiftStartLabel = ttk.Label(self.timeStartFrame, text="Start Time:")
        self.shiftStart = TimePicker(self.timeStartFrame)

        self.timeEndFrame = ttk.Frame(self)
        self.shiftEndLabel = ttk.Label(self.timeEndFrame, text="End Time:")
        self.shiftEnd = TimePicker(self.timeEndFrame)

        self.shiftStartLabel.pack(side="left", pady=5)
        self.shiftStart.pack(side="left", pady=5)

        self.shiftEndLabel.pack(side="left", pady=5)
        self.shiftEnd.pack(side="left", pady=5)

        # Log Button
        self.logButton = ttk.Button(self, text="Log Shift", command=self.logShift)

        # Pack the LogPage Frame
        self.jobLabel.pack()
        self.jobSelectFrame.pack(pady=(0, 15))
        self.timeSelectLabel.pack(pady=(15, 0))
        self.timeStartFrame.pack()
        self.timeEndFrame.pack()
        self.logButton.pack(pady=15)


class ManagerPage(ttk.Frame):
    """Manager-only UI placeholder.

    This application can be extended with manager-facing features.
    """

    def __init__(self, parent, conn, user) -> None:
        """Create the manager page.

        Args:
            parent: The parent Tkinter container.
            conn: Active MySQL connection.
            user: Authenticated User object.

        Return:
            None
        """
        super().__init__(parent)
        # TODO: Implement manager tools (user management, cross-user reports).
        pass


class AdminPage(ttk.Frame):
    """Admin-only UI placeholder.

    This application can be extended with admin-facing features.
    """

    def __init__(self, parent, conn, user) -> None:
        """Create the admin page.

        Args:
            parent: The parent Tkinter container.
            conn: Active MySQL connection.
            user: Authenticated User object.

        Return:
            None
        """
        super().__init__(parent)
        # TODO: Implement admin tools (role assignment, user provisioning).
        pass


class ReportsPage(ttk.Frame):
    def getSearchableBooleans(self):
        # TODO: Validate date inputs and provide UI feedback for invalid ranges.
        if self.startSearch.get():
            startSearch = self.startSearchDate.get_date()
        else:
            startSearch = None

        if self.endSearch.get():
            endSearch = self.endSearchDate.get_date()
        else:
            endSearch = None

        return startSearch, endSearch

    def listShifts(self):
        startSearch, endSearch = self.getSearchableBooleans()

        name, rawHeader, rawData = logic.report_shifts_by_date(
            self.conn,
            self.user,
            self.homeKey.get(),
            self.overtimeKey.get(),
            self.absent.get(),
            startSearch,
            endSearch,
        )
        self.activeReport.set("byDate")

        formatters = {
            "startTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "endTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "hours": lambda h: f"{h:.2f}",
        }

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Full Report by Shift for {name}",
        )

    def byFunction(self):
        name, rawHeader, rawData = logic.report_shifts_by_function(
            self.conn, self.user, self.homeKey.get(), self.overtimeKey.get()
        )
        self.activeReport.set("byFunction")

        formatters = {"hours": lambda h: f"{h:.2f}", "percent": lambda h: f"{h:.2f}"}

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Report by Function for {name}.",
        )

    def byEquipment(self):
        name, rawHeader, rawData = logic.report_shifts_by_equipment(
            self.conn, self.user, self.homeKey.get(), self.overtimeKey.get()
        )
        self.activeReport.set("byEquipment")

        formatters = {"hours": lambda h: f"{h:.2f}", "percent": lambda h: f"{h:.2f}"}

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Report by Equipment for {name}.",
        )

    def timeSince(self):
        name, rawHeader, rawData = logic.report_time_since_functions(
            self.conn, self.user, self.homeKey.get(), self.overtimeKey.get()
        )
        self.activeReport.set("timeSince")

        formatters = {
            "funcDate": lambda d: d.strftime("%Y-%m-%d"),
            "hours": lambda h: f"{h:.2f}",
        }

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Time Since each function for {name}.",
        )

    def missedTime(self):
        startSearch, endSearch = self.getSearchableBooleans()

        name, rawHeader, rawData = logic.report_absences(
            self.conn, self.user, startSearch, endSearch
        )
        self.activeReport.set("Missed Time")

        formatters = {
            "startTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "endTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "hours": lambda h: f"{h:.2f}",
        }

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Report of absences for {name}.",
        )

    def accountableTime(self):
        startSearch, endSearch = self.getSearchableBooleans()
        name, rawHeader, rawData = logic.report_accountable_time(
            self.conn, self.user, startSearch, endSearch
        )
        self.activeReport.set("Accountable Time")

        formatters = {
            "startTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "endTime": lambda d: d.strftime("%Y-%m-%d %H:%M"),
            "hours": lambda h: f"{h:.2f}",
        }

        data, header = dataclassesToRows(rawData, rawHeader, formatters)

        clearTreeview(self.reportView)
        setupTreeview(
            self.reportView,
            header,
            data,
            self.tableLabel,
            f"Report of accountable shifts for {name}.",
        )

    def deleteRow(self, event):
        selectedRow = self.reportView.selection()
        if not selectedRow:
            logger.debug("No row selected for deletion")
        elif self.activeReport.get() != "byDate":
            logger.debug("Can only delete data by date")
        else:
            itemID = selectedRow[0]
            values = self.reportView.item(itemID, "values")
            startTime = datetime.strptime(values[2], "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(values[3], "%Y-%m-%d %H:%M")
            function = values[4]
            isOK = messagebox.askokcancel(
                "WARNING!",
                f"You are about to delete the shift from {startTime} to {endTime} in the function of {function}.  This action cannot be undone.  Are you sure you wish to proceed?",
            )
            if isOK:
                shiftID = logic.get_shift_log_pk(
                    self.conn,
                    self.user,
                    startTime,
                    endTime,
                )
                logic.delete_shift(self.conn, shiftID)
                self.listShifts()

    def editShift(self, event=None):
        selectedRow = self.reportView.selection()
        if not selectedRow:
            logger.debug("No row selected for deletion")
        elif self.activeReport.get() != "byDate":
            logger.debug("Can only delete data by date")
        else:
            itemID = selectedRow[0]
            values = self.reportView.item(itemID, "values")
            startTime = datetime.strptime(values[2], "%Y-%m-%d %H:%M")
            endTime = datetime.strptime(values[3], "%Y-%m-%d %H:%M")
            shiftID = logic.get_shift_log_pk(
                self.conn,
                self.user,
                startTime,
                endTime,
            )
            ShiftEdit(self, shiftID, self.conn, self.user, self.listShifts)

    def updateEditButtonState(self, *args):
        if self.activeReport.get() == "byDate":
            self.editShiftButton.state(["!disabled"])
        else:
            self.editShiftButton.state(["disabled"])

    def __init__(self, parent, conn, user):
        super().__init__(parent)
        self.conn = conn
        self.user = user
        self.pack_configure(fill="both", expand=True)
        self.activeReport = tk.StringVar()
        self.activeReport.set("")

        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.pack(anchor="center", side="top", pady=5)

        self.optionsFrame = ttk.Frame(self)
        self.optionsFrame.pack(anchor="center", side="top", pady=5)

        self.listShiftsButton = ttk.Button(
            self.buttonFrame, text="By Date", command=self.listShifts
        )
        self.timeByFunction = ttk.Button(
            self.buttonFrame, text="By Function", command=self.byFunction
        )
        self.timeByEquipment = ttk.Button(
            self.buttonFrame, text="By Equipment", command=self.byEquipment
        )
        self.timeSinceButton = ttk.Button(
            self.buttonFrame, text="Time Since Functions", command=self.timeSince
        )
        self.absentTime = ttk.Button(
            self.buttonFrame, text="Absences", command=self.missedTime
        )
        self.accountTime = ttk.Button(
            self.buttonFrame, text="Accountable Time", command=self.accountableTime
        )
        self.editShiftButton = ttk.Button(
            self.buttonFrame,
            text="Edit Shift",
            command=self.editShift,
            state="disabled",
        )
        self.listShiftsButton.pack(side="left", padx=5)
        self.timeByFunction.pack(side="left", padx=5)
        self.timeByEquipment.pack(side="left", padx=5)
        self.timeSinceButton.pack(side="left", padx=5)
        self.absentTime.pack(side="left", padx=5)
        self.accountTime.pack(side="left", padx=5)
        self.editShiftButton.pack(side="left", padx=5)

        self.homeKey = tk.BooleanVar(value=1)
        self.overtimeKey = tk.BooleanVar(value=1)
        self.absent = tk.BooleanVar(value=0)
        self.homeKeyBox = ttk.Checkbutton(
            self.optionsFrame, text="Home Key", variable=self.homeKey
        )
        self.overtimeKeyBox = ttk.Checkbutton(
            self.optionsFrame, text="Overtime Key", variable=self.overtimeKey
        )
        self.absentBox = ttk.Checkbutton(
            self.optionsFrame, text="Absences", variable=self.absent
        )
        self.homeKeyBox.pack(side="left", padx=5)
        self.overtimeKeyBox.pack(side="left", padx=5)
        self.absentBox.pack(side="left", padx=5)

        self.startSearch = tk.BooleanVar(value=0)
        self.endSearch = tk.BooleanVar(value=0)

        self.searchDateFrame = ttk.Frame(self)
        self.startSearchCheckbox = ttk.Checkbutton(
            self.searchDateFrame,
            text="Check to use Start Date",
            variable=self.startSearch,
        )
        self.startSearchDate = DateEntry(
            self.searchDateFrame, date_pattern="yyyy-mm-dd"
        )
        self.endSearchCheckbox = ttk.Checkbutton(
            self.searchDateFrame, text="Check to use End Date", variable=self.endSearch
        )
        self.endSearchDate = DateEntry(self.searchDateFrame, date_pattern="yyyy-mm-dd")
        # TODO: Replace magic default date with a configurable constant.
        self.startSearchDate.set_date(date(2025, 1, 1))
        self.endSearchDate.set_date(date.today())

        self.searchDateFrame.pack(anchor="center", side="top", pady=5)
        self.startSearchCheckbox.pack(side="left", padx=5)
        self.startSearchDate.pack(side="left", padx=(5, 40))
        self.endSearchCheckbox.pack(side="left", padx=5)
        self.endSearchDate.pack(side="left", padx=5)

        self.tableLabel = tk.StringVar()
        self.tableLabel.set("")

        self.nameLabel = ttk.Label(
            self, textvariable=self.tableLabel, style="Header.Label"
        )
        self.reportView = ttk.Treeview(self)
        self.nameLabel.pack()
        self.reportView.pack(expand=True, fill="both")
        self.reportView.bind("<Delete>", self.deleteRow)

        self.activeReport.trace_add("write", self.updateEditButtonState)


class TimePicker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.meridiem = tk.StringVar()

        vHour = self.register(self.validateHour)
        vMin = self.register(self.validateMinute)

        self.shiftDateEntry = DateEntry(
            self,
            date_pattern="yyyy-mm-dd",
            year=date.today().year,
            month=date.today().month,
            day=date.today().day,
        )
        self.hourSpin = tk.Spinbox(
            self,
            from_=1,
            to=12,
            width=2,
            validate="key",
            textvariable=self.hour,
            validatecommand=(vHour, "%P"),
        )
        self.colon = ttk.Label(self, text=":")
        self.minuteSpin = tk.Spinbox(
            self,
            from_=0,
            to=59,
            width=2,
            validate="key",
            textvariable=self.minute,
            validatecommand=(vMin, "%P"),
            format="%02.0f",
        )
        self.meridiemBox = ttk.Combobox(
            self,
            values=["AM", "PM"],
            width=3,
            textvariable=self.meridiem,
            state="readonly",
        )
        self.meridiemBox.set("AM")
        self.hour.set("6")
        self.shiftDateEntry.pack(side="left", padx=5)
        self.hourSpin.pack(side="left")
        self.colon.pack(side="left")
        self.minuteSpin.pack(side="left")
        self.meridiemBox.pack(side="left")
        self.setEditable(editable=True)

    def getDateTime(self):
        # TODO: Add input validation with user feedback for empty/invalid time fields.
        hour = int(self.hour.get())
        minute = int(self.minute.get())
        meridiem = self.meridiem.get()

        if meridiem == "PM" and hour != 12:
            hour += 12
        elif meridiem == "AM" and hour == 12:
            hour = 0

        d = self.shiftDateEntry.get_date()
        t = time(hour, minute)
        dt = datetime.combine(d, t)

        return dt

    def setDateTime(self, dt: datetime):
        if dt is None:
            return

        self.shiftDateEntry.set_date(dt.date())

        hour = dt.hour
        minute = f"{dt.minute:02d}"
        meridiem = "AM"

        if hour == 0:
            displayHour = 12
        elif hour < 12:
            displayHour = hour
        elif hour == 12:
            displayHour = 12
            meridiem = "PM"
        elif hour > 12:
            displayHour = hour - 12
            meridiem = "PM"

        self.hour.set(displayHour)
        self.minute.set(minute)
        self.meridiem.set(meridiem)

    def validateHour(self, value):
        if value == "":
            return True
        if not value.isdigit():
            return False
        n = int(value)
        return 1 <= n <= 12

    def validateMinute(self, value):
        if value == "":
            return True
        if not value.isdigit():
            return False
        if len(value) > 2:
            return False
        n = int(value)
        return 0 <= n <= 59

    def setEditable(self, editable: bool):
        state = "normal" if editable else "disabled"

        self.shiftDateEntry.configure(state=state)
        self.hourSpin.configure(state=state)
        self.minuteSpin.configure(state=state)
        self.meridiemBox.configure(state="readonly" if editable else "disabled")


class ShiftEdit(tk.Toplevel):
    def editShift(self, event=None):
        self.newKey = self.editShiftKeyComboBox.get()
        self.newStart = self.editShiftStart.getDateTime()
        self.newEnd = self.editShiftEnd.getDateTime()
        self.newFunc = self.editJobSelection.get()

        if self.newKey == self.oldKey:
            key = None
            keyLog = "No Change"
        else:
            key = self.newKey
            keyLog = f"{self.oldKey} -> {self.newKey}"

        if self.newStart == self.oldStart:
            start = None
            startLog = "No Change"
        else:
            start = self.newStart
            startLog = f"{self.oldStart} -> {self.newStart}"

        if self.newEnd == self.oldEnd:
            end = None
            endLog = "No Change"
        else:
            end = self.newEnd
            endLog = f"{self.oldEnd} -> {self.newEnd}"

        if self.newFunc == self.oldFunc:
            func = None
            funcLog = "No Change"
        else:
            func = self.newFunc.split(" - ", 1)[1]
            funcLog = f"{self.oldFunc} -> {self.newFunc}"

        logger.debug(
            f"Changes to shift: \nKey: {key} \nStart: {start} \nEnd: {end} \nFunction: {func}"
        )

        if any(var is not None for var in (key, start, end, func)):
            result = messagebox.askokcancel(
                "Warning!",
                f"Shift will be changed to the following: \nKey: {keyLog} \nShift Start: {startLog} \nShift End: {endLog} \nFunction: {funcLog}",
            )
            if result:
                logic.edit_shift(self.conn, self.shiftID, start, end, key, func)
                logger.info(
                    f"Shift changed: \nKey: {keyLog} \nShift Start: {startLog} \nShift End: {endLog} \nFunction: {funcLog}"
                )
        else:  # All variables are None
            messagebox.showwarning("Warning!", "No changes were made to the shift.")
            logger.warning("Shift edit requested with no changes made.")

        self.closeWindow()

    def cancelEdit(self, event=None):
        result = messagebox.askokcancel(
            "Warning!", "This will cancel any edits made to this shift, are you sure?"
        )
        if result:
            self.closeWindow()

    def splitConfirm(self, event=None):
        shiftOneStart = self.oldStart
        splitTime = self.splitShiftTime.getDateTime()
        beginJob = self.splitBeginningJob.get()
        endJob = self.splitFinishingJob.get().split(" - ", 1)[1]
        shiftTwoEnd = self.oldEnd
        key = self.oldKey
        shiftID = self.shiftID

        logger.debug("Shift Split Information:")
        logger.debug("Old Shift Start: %s", self.oldStart)
        logger.debug("Old Shift End: %s", self.oldEnd)
        logger.debug("Old Shift Function: %s", self.oldFunc)
        logger.debug("New Shift Split Time: %s", splitTime)
        logger.debug("First Half Job Function: %s", beginJob)
        logger.debug("Second Half Job Function: %s", endJob)

        if beginJob == self.oldFunc:
            beginJob = None
        else:
            beginJob = beginJob.split(" - ", 1)[1]

        if shiftOneStart < splitTime < shiftTwoEnd:
            logic.edit_shift(self.conn, shiftID, None, splitTime, None, beginJob, None)
            logic.log_shift(self.conn, self.user, splitTime, shiftTwoEnd, key, endJob)
        else:
            messagebox.showerror(
                "Error!",
                "The split time must be between the start and end times of the shift.",
            )
            logger.error(
                "Shift Split time %s is not between the old shifts start time %s and finish time %s.",
                splitTime,
                self.oldStart,
                self.oldEnd,
            )

        self.closeWindow()

    def splitShift(self, event=None):
        self.editJobSelectFrame.pack_forget()
        self.splitBeginningJobFrame.configure(padding=(40, 10))
        self.splitTimeFrame.configure(padding=20)
        self.splitShiftButton.pack_forget()

        self.editShiftStart.setDateTime(self.oldStart)
        self.editShiftEnd.setDateTime(self.oldEnd)
        self.editShiftStart.setEditable(False)
        self.editShiftEnd.setEditable(False)

        self.splitTimeLabel = ttk.Label(
            self.splitTimeFrame, text="Choose when the shift split happens."
        )
        self.splitShiftTime = TimePicker(self.splitTimeFrame)
        self.splitTimeLabel.pack()
        self.splitShiftTime.pack()
        self.splitShiftTime.setDateTime(self.oldEnd)

        self.splitBeginningJob = tk.StringVar()
        self.splitFinishingJob = tk.StringVar()
        self.splitBeginningJob.set(self.oldFunc)
        self.splitFinishingJob.set(self.oldFunc)

        self.splitBeginningJobLabel = ttk.Label(
            self.splitBeginningJobFrame,
            text="Select a Job Function for the First Part of the Shift:",
        )
        self.splitBeginningJobSelect = ttk.Combobox(
            self.splitBeginningJobFrame,
            textvariable=self.splitBeginningJob,
            values=self.editJobs,
            state="readonly",
        )
        self.splitBeginningJobLabel.pack()
        self.splitBeginningJobSelect.pack()

        self.splitFinishingJobLabel = ttk.Label(
            self.splitFinishingJobFrame,
            text="Select a Job Function for the Second Part of the Shift:",
        )
        self.splitFinishingJobBox = ttk.Combobox(
            self.splitFinishingJobFrame,
            textvariable=self.splitFinishingJob,
            values=self.editJobs,
            state="readonly",
        )
        self.splitFinishingJobLabel.pack()
        self.splitFinishingJobBox.pack()

        self.submitButton.configure(command=self.splitConfirm)

    def closeWindow(self, event=None):
        if self.cbFunc:
            self.cbFunc()
        self.destroy()

    def __init__(self, parent, shiftID, conn, user, cbFunc):
        super().__init__(parent)
        self.conn = conn
        self.user = user
        self.shiftID = shiftID
        self.cbFunc = cbFunc

        self.geometry("500x600")
        self.title("Shift Editor")

        shiftData = logic.get_shift_log_row(self.conn, self.shiftID)

        self.editShiftInfoFrame = ttk.Frame(self)
        self.editShiftInfoFrame.pack(anchor="center")
        self.editShiftHeaderLabel = ttk.Label(
            self.editShiftInfoFrame,
            text="This is the shift you are editing.",
            justify="center",
            style="Header.Label",
        )

        self.editKeyLabel = ttk.Label(self.editShiftInfoFrame, text="Key")
        self.editStartTimeLabel = ttk.Label(self.editShiftInfoFrame, text="Start Time")
        self.editEndTimeLabel = ttk.Label(self.editShiftInfoFrame, text="End Time")
        self.editFunctionLabel = ttk.Label(self.editShiftInfoFrame, text="Function")
        if shiftData:
            self.oldKey = shiftData.shiftID
            self.oldStart = shiftData.timeStarted
            self.oldEnd = shiftData.timeFinished
            self.oldFunc = f"{shiftData.funcType} - {shiftData.funcName}"

        self.editKeyDisplay = ttk.Label(self.editShiftInfoFrame, text=self.oldKey)
        self.editStartTimeDisplay = ttk.Label(
            self.editShiftInfoFrame, text=self.oldStart
        )
        self.editEndTimeDisplay = ttk.Label(self.editShiftInfoFrame, text=self.oldEnd)
        self.editFunctionDisplay = ttk.Label(self.editShiftInfoFrame, text=self.oldFunc)

        self.editShiftHeaderLabel.grid(row=0, column=0, columnspan=4)
        self.editKeyLabel.grid(row=1, column=0, padx=10)
        self.editStartTimeLabel.grid(row=1, column=1, padx=10)
        self.editEndTimeLabel.grid(row=1, column=2, padx=10)
        self.editFunctionLabel.grid(row=1, column=3, padx=10)
        self.editKeyDisplay.grid(row=2, column=0, padx=10)
        self.editStartTimeDisplay.grid(row=2, column=1, padx=10)
        self.editEndTimeDisplay.grid(row=2, column=2, padx=10)
        self.editFunctionDisplay.grid(row=2, column=3, padx=10)

        # Job Function Selection and Key
        self.editJobMap = logic.get_jobs(self.conn)
        self.editJobs = list(self.editJobMap.keys())
        self.editSelectedJob = tk.StringVar()

        self.editJobSelectFrame = ttk.Frame(self)
        self.editJobSelectFrame.pack(anchor="center", pady=(40, 10))
        self.editJobLabel = ttk.Label(
            self.editJobSelectFrame, text="Select Job Function"
        )
        self.editJobSelection = ttk.Combobox(
            self.editJobSelectFrame,
            textvariable=self.editSelectedJob,
            values=self.editJobs,
            state="readonly",
        )
        self.editJobLabel.pack(side="left")
        self.editJobSelection.pack(side="left")

        self.editShifts = logic.get_shifts(self.conn)
        self.editSelectedShift = tk.StringVar()

        self.editShiftKeyLabel = ttk.Label(self.editJobSelectFrame, text="Enter Key:")
        self.editShiftKeyComboBox = ttk.Combobox(
            self.editJobSelectFrame,
            textvariable=self.editSelectedShift,
            values=self.editShifts,
            state="readonly",
            width=3,
        )

        self.editShiftKeyLabel.pack(side="left", padx=(10, 0))
        self.editShiftKeyComboBox.pack(side="left")

        # Start / End Time
        self.editTimeSelectLabel = ttk.Label(
            self,
            text="Enter the Start and Finish Time of the job function",
            justify="center",
        )
        self.editTimeSelectLabel.pack(anchor="center", pady=(10, 0))

        self.splitBeginningJobFrame = ttk.Frame(self)
        self.splitBeginningJobFrame.pack(anchor="center")

        self.editTimeStartFrame = ttk.Frame(self)
        self.editTimeStartFrame.pack(anchor="center", pady=(10, 0))
        self.editShiftStartLabel = ttk.Label(
            self.editTimeStartFrame, text="Start Time:"
        )
        self.editShiftStart = TimePicker(self.editTimeStartFrame)

        self.splitTimeFrame = ttk.Frame(self)
        self.splitTimeFrame.pack(anchor="center")

        self.splitFinishingJobFrame = ttk.Frame(self)
        self.splitFinishingJobFrame.pack(anchor="center")

        self.editTimeEndFrame = ttk.Frame(self)
        self.editTimeEndFrame.pack(anchor="center", pady=(10, 0))
        self.editShiftEndLabel = ttk.Label(self.editTimeEndFrame, text="End Time:")
        self.editShiftEnd = TimePicker(self.editTimeEndFrame)

        self.editShiftStartLabel.pack(side="left", pady=5)
        self.editShiftStart.pack(side="left", pady=5)

        self.editShiftEndLabel.pack(side="left", pady=5)
        self.editShiftEnd.pack(side="left", pady=5)

        value = f"{shiftData.funcType} - {shiftData.funcName}"
        if value in self.editJobSelection["values"]:
            self.editSelectedJob.set(value)
        else:
            logger.warning("Combobox value not found: %s", value)

        self.editSelectedShift.set(shiftData.shiftID)
        self.editShiftStart.setDateTime(shiftData.timeStarted)
        self.editShiftEnd.setDateTime(shiftData.timeFinished)

        self.buttonFrame = ttk.Frame(self)
        self.buttonFrame.pack(pady=20)

        self.submitButton = ttk.Button(
            self.buttonFrame, text="Confirm Edit", command=self.editShift
        )
        self.cancelButton = ttk.Button(
            self.buttonFrame, text="Cancel Edit", command=self.cancelEdit
        )
        self.splitShiftButton = ttk.Button(
            self.buttonFrame, text="Split Shift", command=self.splitShift
        )
        self.submitButton.pack(side="left", padx=20)
        self.cancelButton.pack(side="left", padx=20)
        self.splitShiftButton.pack(side="left", padx=20)
