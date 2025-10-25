# This is the Main Program, it contains the main GUI, the login, and some other logics.

import tkinter as tk
from tkinter import ttk, messagebox
from wwGUI import WarehouseWorkerGUI

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Warehouse Management System")
root.geometry("1100x900+400+50")
root.resizable(width=False, height=False)

buttonFrame = ttk.Frame(root)
buttonFrame.pack(side="top", fill="x", pady=5)

notebookFrame = ttk.Frame(root)
notebookFrame.pack(fill="both", expand=True)

def wwTab():
    clear_frame(notebookFrame)
    app = WarehouseWorkerGUI(root, notebookFrame)

def imTab():
    messagebox.showinfo("Success", "You pressed the Inventory Manager Functions Button")

def locTab():
    messagebox.showinfo("Success", "You pressed the Warehouse Locations Button")

def omTab():
    messagebox.showinfo("Success", "You pressed the Operations Manager Functions Button")

def logout():
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        clear_frame(notebookFrame)
        clear_frame(buttonFrame)
        login_screen()

def quitprogram():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()  # Close the window if user clicks Yes

def createButtons():    
    wwButton = ttk.Button(buttonFrame, text="Warehouse Worker Functions", command=wwTab)
    wwButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
    imButton = ttk.Button(buttonFrame, text="Inventory Manager Functions", command=imTab)
    imButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
    locButton = ttk.Button(buttonFrame, text="Warehouse Location Functions", command=locTab)
    locButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
    omButton = ttk.Button(buttonFrame, text="Operations Manger Functions", command=omTab)
    omButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
    logoutButton = ttk.Button(buttonFrame, text="Logout", command=logout)
    logoutButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)
    quitButton = ttk.Button(buttonFrame, text="Quit", command=quitprogram)
    quitButton.pack(side="left", expand=True, fill="x", padx=2, pady=5)

def login():
    # verify username and ID function tbd
    user = username.get()
    messagebox.showinfo("Success", f"Welcome {user}!")
    clear_frame(notebookFrame)
    createButtons()
    wwTab()

username = tk.StringVar()
password = tk.StringVar()
def login_screen():
    usernameLabel = ttk.Label(notebookFrame, text="Username")
    usernameLabel.pack(pady=(300, 0))
    usernameEntry = ttk.Entry(notebookFrame, textvariable=username)
    usernameEntry.pack()
    passwordLabel = ttk.Label(notebookFrame, text="Password")
    passwordLabel.pack(pady=(15, 0))
    passwordEntry = ttk.Entry(notebookFrame, textvariable=password, show="*")
    passwordEntry.pack()
    loginButton = ttk.Button(notebookFrame, text="Login", command=login)
    loginButton.pack(pady=(15,0))
    quitButton = ttk.Button(notebookFrame, text="Quit", command=quitprogram)
    quitButton.pack(pady=(15,0))

login_screen()
root.mainloop()