import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import db
import utils

class GUI():
    def __init__(self, master, conn):
        self.master = master
        self.master.title("Work Job Tracker")
        self.master.geometry("600x400")

        self.style = ttk.Style()
        self.style.theme_use('aqua')
        
        self.style.configure("Quit.TButton", foreground="firebrick1", font=("Arial", 12, "bold"))

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True)
        self.quitButton = ttk.Button(master, text="EXIT", command=master.destroy, style="Quit.TButton")
        self.notebook.pack()
        self.quitButton.pack(side="bottom", pady=10)

        self.logPage = LogPage(self.notebook, conn)
        self.reportsPage = ReportsPage(self.notebook, conn)

        self.notebook.add(self.logPage, text="Log Shift")
        self.notebook.add(self.reportsPage, text="Reports")

class LogPage(ttk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.pack_configure(fill="both", expand=True)
        self.conn = conn

        # Select the Job Function
        jobs = db.getJobs()
        selectedJob = tk.StringVar()
        jobLabel = ttk.Label(self, text="Select Job Function")
        jobSelection = ttk.Combobox(self, textvariable=selectedJob, values=jobs, state="readonly")
        jobLabel.grid(column=0, row=0, columnspan=5)
        jobSelection.grid(column=0, row=1, columnspan=5)

        # Select Shift Date and Shift
        shifts = db.getShifts()
        selectedShift = tk.StringVar()
        shiftDateLabel = ttk.Label(self, text="Enter Date of the Shift:")
        shiftDateEntry = DateEntry(self, date_pattern="yyyy-mm-dd")
        shiftKeyLabel = ttk.Label(self, text="Enter Key: ")
        shiftKeyComboBox = ttk.Combobox(self, textvariable=selectedShift, values=shifts, state="readonly")
        shiftDateLabel.grid(column=0, row=2, pady=5)
        shiftDateEntry.grid(column=2, row=2, pady=5)
        shiftKeyLabel.grid(column=3, row=2, pady=5)
        shiftKeyComboBox.grid(column=4, row=2, pady=5)

        # Select the Start and End Time
        timeSelectLabel = ttk.Label(self, text="Enter the Start and Finish Time of the job function")
        shiftStartLabel = ttk.Label(self, text="Start Time: ")
        shiftStart = TimePicker(self)
        shiftEndLabel = ttk.Label(self, text="End Time:")
        shiftEnd = TimePicker(self)

        timeSelectLabel.grid(column=0, row=3, pady=(20,5), columnspan=5)
        shiftStartLabel.grid(column=0, row=4, pady=5)
        shiftStart.grid(column=1, row=4, columnspan=3, pady=5)
        shiftEndLabel.grid(column=0, row=5, pady=5)
        shiftEnd.grid(column=1, row=5, pady=5)


class ReportsPage(ttk.Frame):
    def __init__(self, parent, conn):
        super().__init__(parent)
        self.conn = conn
        self.pack_configure(fill="both", expand=True)

class TimePicker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.hour = tk.StringVar()
        self.minute = tk.StringVar()
        self.meridiem = tk.StringVar()

        vHour = self.register(self.validateHour)
        vMin = self.register(self.validateMinute)

        self.hourSpin = tk.Spinbox(self, from_=1, to=12, width=2, validate="key", textvariable=self.hour, validatecommand=(vHour, "%P"))
        self.colon = ttk.Label(self, text=":")
        self.minuteSpin = tk.Spinbox(self, from_=0, to=59, width=2, validate="key", textvariable=self.minute, validatecommand=(vMin, "%P"), format="%02.0f")
        self.meridiemBox = ttk.Combobox(self, values=["AM", "PM"], width=3, textvariable=self.meridiem, state="readonly")
        self.meridiemBox.set("AM")
        self.hourSpin.grid(column=0, row=0)
        self.colon.grid(column=1, row=0)
        self.minuteSpin.grid(column=2, row=0)
        self.meridiemBox.grid(column=3, row=0)


    def getTime(self):
        hour = self.hour.get()
        minute = self.minute.get()
        meridiem = self.meridiem.get()

        if meridiem == "PM":
            hour +=12
        
        minute = 60/minute
        time = hour + minute
        return time


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


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Work Job Tracker GUI")

    conn = db.getConn()

    gui = GUI(root, conn)
    root.mainloop()