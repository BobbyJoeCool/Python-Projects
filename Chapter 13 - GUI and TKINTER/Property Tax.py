'''
A county collects property taxes on the assessment value of property, 
which is 60 percent of the property’s actual value. 
If an acre of land is valued at $10,000, its assessment value is $6,000. 
The property tax is then $0.75 for each $100 of the assessment value. 
The tax for the acre assessed at $6,000 will be $45.00. 
Write a GUI program that displays the assessment value and property tax 
when a user enters the actual value of a property.
'''

import tkinter as tk

# Create the Root Window
root = tk.Tk()
root.title("Property Tax Calculator")
root.attributes("-topmost", True)
root.geometry("+400+400")

# Create the Variables needed for the program
rate = .75/100
assessCoef = 6000/10000
propertyValue = tk.IntVar()
message = tk.StringVar()

# Create the 3 Frames: Property Value, Assessed Value/Tax Owed, Buttons
entryFrame = tk.Frame(root)
displayFrame = tk.Frame(root)
buttonFrame = tk.Frame(root)
entryFrame.pack(pady=5)
displayFrame.pack(pady=5)
buttonFrame.pack(pady=5)

# Function to calculate the Assessed Value and Tax Value
def calculate_value():
    try:
        val = propertyValue.get()
        if val <= 0:
            message.set("Error, please enter a positive integer for the assessed value.")
        else:
            assessedValue = round(val*assessCoef)
            taxValue = assessedValue * rate
            message.set(f"Your Assessed Value is ${assessedValue:,}.\nYour Annual Property Tax is ${taxValue:,.2f}.")
    except tk.TclError:
        message.set("Error, please enter a valid number for the assessed value.")

# Create the Entry Frame
valueLabel = tk.Label(entryFrame, text="Enter the Property Value:  $")
valueLabel.pack(side="left")
valueEntry = tk.Entry(entryFrame, textvariable=propertyValue)
valueEntry.pack(side="right")

# Create the Display Frame
displayLabel = tk.Label(displayFrame, textvariable=message).pack()

# Create the Button Frame
calculateButton = tk.Button(buttonFrame, text="Calculate", command=calculate_value)
calculateButton.pack(side="left", padx=20)
quitButton = tk.Button(buttonFrame, text="Quit", command=root.destroy)
quitButton.pack(side="right", padx=20)

# Run the Main Program
root.mainloop()