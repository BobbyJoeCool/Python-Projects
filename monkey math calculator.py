# This program does "Monkey Math" which is a fancy way of saying concatenation.

import tkinter as tk

# Creates Main Window
root = tk.Tk()
root.title("Monkey Math Calculator")
root.geometry("300x200+600+400")
root.attributes("-topmost", True)

# Frame Creation
entryFrame = tk.Frame(root)
entryFrame.pack(pady=10)
resultFrame = tk.Frame(root)
resultFrame.pack(pady=10)
buttonFrame = tk.Frame(root)
buttonFrame.pack(pady=10)

# Variables Needed for Widgets
num1 = tk.StringVar()
num2 = tk.StringVar()
result = tk.StringVar()

# Entry Frame Widgets
num1Label = tk.Label(entryFrame, text="Number 1")
num2Label = tk.Label(entryFrame, text="Number 2")
num1Label.grid(row=0, column=0)
num2Label.grid(row=0, column=2)
num1Entry = tk.Entry(entryFrame, textvariable=num1, width=5)
numOperator = tk.Label(entryFrame, text=" + ")
num2Entry = tk.Entry(entryFrame, textvariable=num2, width=5)
num1Entry.grid(row=1, column=0)
numOperator.grid(row=1, column=1)
num2Entry.grid(row=1, column=2)

# Result Frame
resultLabel = tk.Label(resultFrame, textvariable=result)
resultLabel.pack()

# Button Widgets and Function
def calculate(event=None):
    n1 = num1.get()
    n2 = num2.get()
    if n1 == "" or n2 == "":
        return
    res = n1 + n2
    result.set(f"{n1} + {n2} = {res}")
    num1.set("")
    num2.set("")

num1Entry.bind("<Return>", calculate)
num2Entry.bind("<Return>", calculate)

calcButton = tk.Button(buttonFrame, text="Calculate", command=calculate)
calcButton.grid(row=1, column=0)
quitButton = tk.Button(buttonFrame, text="Quit", command=root.destroy)
quitButton.grid(row=1, column=1)

root.mainloop()