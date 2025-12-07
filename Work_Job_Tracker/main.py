import tkinter as tk
from gui import GUI
from db import getConn

def main():
    conn = getConn()
    if conn:
        root = tk.Tk()
        app = GUI(root, conn)
        root.mainloop()
        conn.close()

if __name__ == "__main__":
    main()