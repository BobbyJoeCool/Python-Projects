'''
Write a GUI program that calculates a car’s gas mileage. 
The program’s window should have Entry widgets that let the user enter the number of gallons of 
gas the car holds, and the number of miles it can be driven on a full tank. 
When a Calculate MPG button is clicked, the program should display the number of miles 
that the car may be driven per gallon of gas. Use the following formula to calculate miles-per-gallon:
'''

import tkinter as tk

# Create the Main Window
root = tk.Tk()
root.title("MPG Calculator")
root.attributes("-topmost", True)
root.geometry("+500+500")

# Create the frames for the GUI, 1 for each entry field, 1 for the output field, and one for the buttons
milesFrame = tk.Frame(root, pady=10)
gallonsFrame = tk.Frame(root, pady=10)
displayFrame = tk.Frame(root, pady=10)
buttonFrame = tk.Frame(root, pady=10)
milesFrame.pack()
gallonsFrame.pack()
displayFrame.pack()
buttonFrame.pack()

# Create the Float Variables to use for the program
miles = tk.DoubleVar()
gallons = tk.DoubleVar()
mpg= tk.StringVar()

# Fucntion to calculate mpg
def calculate_mpg():
    try:
        g = gallons.get()
        m = miles.get()
        if g == 0:
            mpg.set("Error: gallons cannot be 0")
        elif g < 0 or m < 0:
            mpg.set("Error: miles and gallons must be positive")
        else:
            mpg_value = m/g
            mpg.set(f"You get {mpg_value:.2f} per gallon")
    except tk.TclError:
        mpg.set("Error: Please enter valid numeric values.")

# Create the miles label and entry field
milesLabel = tk.Label(milesFrame, text="Enter the number of miles you get on a full tank:")
milesEntry = tk.Entry(milesFrame, textvariable=miles)
milesLabel.pack(side="left", padx=5)
milesEntry.pack(side="right", padx=5)

# Create the gallons label and entry field
gallonsLabel = tk.Label(gallonsFrame, text="Enter the number of gallons your tank holds:")
gallonsEntry = tk.Entry(gallonsFrame, textvariable=gallons)
gallonsLabel.pack(side="left", padx=5)
gallonsEntry.pack(side="right", padx=5)

# Create the calulation display field
displayLabel = tk.Label(displayFrame, textvariable=mpg)
displayLabel.pack()

# Create the buttons 
calculateButton = tk.Button(buttonFrame, text="Calculate", command=calculate_mpg)
quitButton = tk.Button(buttonFrame, text="Exit", command=root.destroy)
calculateButton.pack(side="left", padx=40)
quitButton.pack(side="right", padx=40)

root.mainloop()