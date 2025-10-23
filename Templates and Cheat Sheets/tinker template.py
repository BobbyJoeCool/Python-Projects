#This contains the template for using TKINTER to make a GUI.

import tkinter as tk
from tkinter import ttk
#by using the "as tk" everytime you need to call for tkinter, you can call for tk instead.

#Creates a class for the GUI, all aspects of the GUI will take place within the class.
#Then create an instance of the class to activate the GUI.
class GUI:
    def __init__(self):
        self.main_window = tk.Tk() # Creates the Main Window
        
        self.main_window.title("Tk Example") # Sets the title of the GUI Window
        self.main_window.configure(bg="black") # Sets the Background of the GUI Window
        self.main_window.minsize(200, 200) # Sets the Minimum Size
        self.main_window.maxsize(500, 500) # Sets the Maximum Size
        self.main_window.geometry("300x300+50+50") # (height+width+x coord+y coord)

        # Creates the frames for each of the wigets used in this example
        self.label_frame = tk.Frame(self.main_window, bg="lightblue") # Creates a Light Blue Frame
        self.label_frame.pack()
        self.check_frame = tk.Frame(self.main_window, bg="blue") # Creates a Blue Frame
        self.check_frame.pack()
        self.combo_frame = tk.Frame(self.main_window, bg="green") # Creates a Green Frame
        self.combo_frame.pack()

        # A list of the Widgets.
        widgets = [
        tk.Label, # This allows you to put text in the widget
        tk.Checkbutton, # Allows for a user Checkbox
        ttk.Combobox, # Creates a Dropdown 
        tk.Entry, # Allows for a user to enter text.
        tk.Button, # Creates a button that can be pressed.
        tk.Radiobutton, # Creates a Radio Button
        tk.Scale, # Creates a Slider scale the user can move.
        tk.Spinbox, # Creates an Integer Spinner
        ]

        # Example Label Widget
        label = tk.Label(self.label_frame, text="Hello", font=("Helvetica", 30), bg="lightblue", fg="black") # Makes a label showing Hello
        label.config(text="This is a Test") # Changes the text to Goodbye
        label.config(anchor="w") # Aligns test to the "west (left)" of the screen ("center" for center) 
        label.pack(padx=5, pady=5)

        # Example Checkbutton Widget
        # This function sets the label to Checked when the box is Checked, and Unchecked when it isn't.
        def show_state(): 
            checked = "Checked" if cked.get() else "Unchecked"
            checkbox.config(text=f"Check me! ({checked})")

        cked = tk.IntVar() # Sets up the cked variable 
        checkbox = tk.Checkbutton(self.check_frame, text="Check me! (Checked)", bg="blue", variable=cked)
        checkbox.select() # Selects the checkbox, Deselect deselects the box.
        checkbox.config(command = show_state) # This calls the function "show_state" when the checkbox is ticked.
        checkbox.pack(padx=5, pady=10, anchor="w")

        # Example Dropdown Widget
        def dd_selection_changed(event):
            label2.config(text=f"{event.widget.get()} selected!")
        
        label2 = tk.Label(self.combo_frame, text="Alpha Selected", bg="green")
        combobox = ttk.Combobox(self.combo_frame, values=["Alpha", "Beta", "Gamma"])
        combobox.set("Alpha")
        combobox.bind("<<ComboboxSelected>>", dd_selection_changed) # This calls the function when the selection changes.
        combobox.pack(padx=5, pady=5, fill="x", anchor="s")
        label2.pack(anchor="n")

        # Listbox Widget
        def lb_selection_changed(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                label.config(text=f"{event.widget.get(index)} selected!")
                event.widget.get(index)

        listbox = tk.Listbox(root)
        for item in ["Alpha", "Beta", "Gamma"]:
            listbox.insert(tk.END, item)
        listbox.bind("<<ListboxSelect>>", lb_selection_changed)
        listbox.pack(padx=5, pady=5, fill="both", expand=True)

        # A helper label to show the selected value
        label = tk.Label(root, text="One selected!")
        label.pack(padx=5, pady=5, fill="x")

        self.main_window.mainloop()

GUI()