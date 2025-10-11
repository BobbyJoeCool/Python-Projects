'''
Write a GUI program that displays your name and address when a button is clicked. 
The program’s window should appear as the sketch on the left side of Figure 13-61 when it runs. 
When the user clicks the Show Info button, the program should display your name and address, 
as shown in the sketch on the right of the figure.
'''

import tkinter as tk

#Create the Main Window
root = tk.Tk()
root.title("Name and Address")
root.geometry("+500+500")
root.attributes("-topmost", True)
root.configure(bg="black")

# Create and pack frame to display the address in the top of the window
display_frame = tk.Frame(root, bg="black", padx=10, pady=10)
display_frame.pack(anchor="n")

# Create and pack frame for the buttons in the bottom of the window
button_frame = tk.Frame(root, bg="black", padx=10, pady=10)
button_frame.pack(anchor="s")

# Creates the nessecary Labels for the program
buttonLabel = tk.StringVar()
buttonLabel.set("Show Info")
name = tk.StringVar()
streetAddress = tk.StringVar()
cityState = tk.StringVar()

# Fuction for the SHOW/HIDE button.
def show_info():
    if name.get() == "":
        name.set("Robert Breutzmann")
        streetAddress.set("508 S Main Street")
        cityState.set("Tripoli, IA 50676")
        buttonLabel.set("Hide Info")
    else:
        name.set("")
        streetAddress.set("")
        cityState.set("")
        buttonLabel.set("Show Info")

# Create the labels and pack them in the upper frame
nameLabel = tk.Label(display_frame, textvariable=name, bg="black", fg="white")
streetLabel = tk.Label(display_frame, textvariable=streetAddress, bg="black", fg="white")
cityLabel = tk.Label(display_frame, textvariable=cityState, bg="black", fg="white")
nameLabel.pack()
streetLabel.pack()
cityLabel.pack()

# Create and pack the buttons for the bottom of the program
showHide = tk.Button(button_frame, textvariable=buttonLabel, command=show_info)
quitButton = tk.Button(button_frame, text="Exit", command=root.destroy)
showHide.pack(side="left", padx=30)
quitButton.pack(side="right", padx=30)

root.mainloop()