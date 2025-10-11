'''
Joe's Automotive performs the following routine maintenance services:
Oil change—$30.00
Lube job—$20.00
Radiator flush—$40.00
Transmission flush—$100.00
Inspection—$35.00
Muffler replacement—$200.00
Tire rotation—$20.00
Write a GUI program with check buttons that allow the user to select any or all of these services. When the user clicks a button, the total charges should be displayed.
'''

import tkinter as tk

# Create the Main Window
root = tk.Tk()
root.title("Joe's Automotive")
root.geometry("+700+400")
root.attributes("-topmost", True)

# Create Frames: Top Label, Grid of Services, Display Frame, Quit Frame
topFrame = tk.Frame(root)
servicesFrame = tk.Frame(root)
displayFrame = tk.Frame(root)
quitFrame = tk.Frame(root)
topFrame.pack(pady=5)
servicesFrame.pack(pady=5)
displayFrame.pack(pady=5)
quitFrame.pack(pady=5)

# Create Top Label
titleLabel = tk.Label(topFrame, text="Joe's Automotive Services", font=("",24))
descriptionLabel = tk.Label(topFrame, text="Select the services you need")
titleLabel.pack()
descriptionLabel.pack()

# Create the Calculate Total Function for whan a total is calculated
def calculate_total():
    total = sum (price for service, price in services.items() if service_vars[service].get() == 1)
    displayMessage.set(f"Total: ${total:.2f}")

# Create Variables needed for the functions
services = {"Oil Change": 30,
            "Lube Job": 20,
            "Radiator Flush": 40,
            "Transmission Flush": 100,
            "Inspection": 35,
            "Muffler Replacement": 200,
            "Tire Rotation": 20}

service_vars = {}

displayMessage = tk.StringVar()
displayMessage.set("Total: $0.00")

# Create Checkboxes in Frames and align in Grid
for i, (service, price) in enumerate(services.items()):
    var = tk.IntVar()
    chk = tk.Checkbutton(servicesFrame, text=f"{service} (${price})", variable=var, command=calculate_total)
    chk.grid(row=i % 4, column=i // 4, sticky="w", padx=10, pady=2)
    service_vars[service] = var

# Create Display Box showing total price.
displayLabel = tk.Label(displayFrame, textvariable=displayMessage, font=("", 18, "bold")).pack()

# Create Quit Button
quitButton = tk.Button(quitFrame, text="Quit", command=root.destroy).pack()

# Run Mainloop
root.mainloop()