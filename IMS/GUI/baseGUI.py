import tkinter as tk
from tkinter import ttk, messagebox
from .wwGUI import WarehouseWorkerGUI
from .lmGUI import LocationManagerGUI

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

class BaseGUI():
    def __init__(self, root):
        self.root = root
        self.setup_frames()
        self.setup_variables()
        self.login_screen()

    def setup_frames(self):
        self.buttonFrame = ttk.Frame(self.root)
        self.buttonFrame.pack(side="top", fill="x", pady=5)

        self.notebookFrame = ttk.Frame(self.root)
        self.notebookFrame.pack(fill="both", expand=True)

    def setup_variables(self):
        self.username = tk.StringVar()
        self.password = tk.StringVar()

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def wwTab(self):
        self.clear_frame(self.notebookFrame)
        self.app = WarehouseWorkerGUI(self.root, self.notebookFrame)

    def imTab(self):
        messagebox.showinfo("Success", "You pressed the Inventory Manager Functions Button")

    def locTab(self):
        self.clear_frame(self.notebookFrame)
        self.app = LocationManagerGUI(self.root, self.notebookFrame)

    def omTab(self):
        messagebox.showinfo("Success", "You pressed the Operations Manager Functions Button")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.clear_frame(self.notebookFrame)
            self.clear_frame(self.buttonFrame)
            self.login_screen()

    def quitprogram(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.destroy()  # Close the window if user clicks Yes

    def createButtons(self):    
        wwButton = ttk.Button(self.buttonFrame, text="Warehouse Worker Functions", command=self.wwTab)
        wwButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
        imButton = ttk.Button(self.buttonFrame, text="Inventory Manager Functions", command=self.imTab)
        imButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
        locButton = ttk.Button(self.buttonFrame, text="Warehouse Location Functions", command=self.locTab)
        locButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
        omButton = ttk.Button(self.buttonFrame, text="Operations Manger Functions", command=self.omTab)
        omButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
        logoutButton = ttk.Button(self.buttonFrame, text="Logout", command=self.logout)
        logoutButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
        quitButton = ttk.Button(self.buttonFrame, text="Quit", command=self.quitprogram)
        quitButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)

    def login(self):
        # verify username and ID function tbd
        user = self.username.get()
        messagebox.showinfo("Success", f"Welcome {user}!")
        self.clear_frame(self.notebookFrame)
        self.createButtons()
        self.wwTab()

    def login_screen(self):
        usernameLabel = ttk.Label(self.notebookFrame, text="Username")
        usernameLabel.pack(pady=(300, 0))
        usernameEntry = ttk.Entry(self.notebookFrame, textvariable=self.username)
        usernameEntry.pack()
        passwordLabel = ttk.Label(self.notebookFrame, text="Password")
        passwordLabel.pack(pady=(15, 0))
        passwordEntry = ttk.Entry(self.notebookFrame, textvariable=self.password, show="*")
        passwordEntry.pack()
        loginButton = ttk.Button(self.notebookFrame, text="Login", command=self.login)
        loginButton.pack(pady=(15,0))
        quitButton = ttk.Button(self.notebookFrame, text="Quit", command=self.quitprogram)
        quitButton.pack(pady=(15,0))