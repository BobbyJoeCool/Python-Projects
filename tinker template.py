#This contains the template for using TKINTER to make a GUI.

import tkinter as tk
from tkinter import ttk
#by using the "as tk" everytime you need to call for tkinter, you can call for tk instead.

#Creates a class for the GUI, all aspects of the GUI will take place within the class.
#Then create an instance of the class to activate the GUI.
class GUI:
    def __init__(self):
        self.root = tk.Tk()		 	            # Creates a window named “root”
        self.root.title("Window Title")           # Makes the Window's Title
        self.root.geometry("300x300+200+200") 	# Sets size and position (Width x Height + x position + y Position)
        self.root.attributes("alpha", 1.0) 	    # Allows setting attributes
	        # “-alpha”, value (0.0 to 1.0)	Controls transparency
	        # “-topmost”, True/False	Makes it stay on top
	        # “-fullscreen”, True/False 	Toggles fullscreen mode
        self.root.resizeable(width=True, height=True)   # Lets you resize the window (Default is True)
        self.root.iconphoto(True, PhotoImage_Object)   # Sets the Window Icon
        self.root.destroy()         # Closes the window
        self.root.withdraw()        # Hides the window (not destroys)
        self.root.deiconify()	    # Restores a hidden or minimized window
        self.root.lift()		    # Bring the window to the front
        self.root.update()	        # Forces tkinter to process pending events
        self.root.mainloop()	    # Starts the eventloop, listening for events.
    
    frame = tk.Frame(root, width=100, height=100, bg="red", relief="solid", padx=10, pady=10).  #Creates a frame
	    # width, height	Creates dimensions of the frame
	    # bg or background	Background color
	    # bd or borderwidth	Width of the Border around frame
	    # relief		Style of the border
	    # cursor	changes mouse appearance when over frame
	    # padx, pady	creates padding around the frame
    
    frame.grid(root, column=1, row=2, columspan=2, sticky="N")	# sets the item into a grid
        # column	        the col number the widget occupies, start at 0.
        # columnspan	    number of columns the widget takes
        # in_		        register widget as a child
        # ipadx, ipady	    internal padding
        # padx, pady	    external padding
        # row	            the row number the widget occupies, start at 0.
        # rowspan		    number of rows the widget takes
        # sticky	        determines how to stick in a cell
	                # uses N, NE, S, SE method.
            # To make it stretch to fit, use E+W to stretch horizontally.
            # To make it stretch to fit, use N+S to stretch vertically.

    frame.pack(root, anchor="N", padx=10, pady=10)	# packs the item
	    # expand (0, or 1)	    should expand to fill space
	    # fill                  (NONE, X, Y, BOTH) How to resize as child
	    # side                  (TOP, BOTTOM, RIGHT, LEFT)
		                # Which side of the parent is used for child
        # in_		            register widget as a child
        # ipadx, ipady	        internal padding
        # padx, pady	        external padding
        # anchor		        Specifies where it should be placed
	                    # uses N,S,E,W,CENTER syntax

    
    frame.place(root, x=150, y=350)	# places the item
        #anchor		                            Specifies where it should be placed
	        # used N,S,E,W,CENTER syntax
        # bordermode (INSIDE, OUTSIDE)          specifies if the border should be inside or outside
        # in_		                            register widget as a child
	    # relwidth, relheight Float [0.0, 1.0]  size of the child widget related to the parent
	    # relx, rely Float [0.0, 1.0]           position of the child widget related to the parent
	    # width, height	                        Absolute height/width of widget
	    # x, y		                            Absolute position of the widget

    # Using variables in Tkinter
    var = IntVar()		        # creates an Integer Variable
    var = FloatVar()		    # creates a Float Variable
    var = StringVar()		    # creates a String Variable
    var = BooleanVar()		    # creates a Boolean Variable

    var.get()			                        # returns the current value
    var.set(x)			                        # sets the value to x
    var.trace_add(“mode”, callback)             # calls function when var changes
    var.trace_remove(“mode”, callback_name)     #removes a trace callback
	    # modes: 	
            # write – when the variable is modified
		    # read – when the variable is read
		    # unset – when the variable is deleted

    # Common Widget Methods
    config(attrubute)		# configure options after creation
    cget(attribute)		    # gets value of an option
    destroy()			    # removes the widget
    bind(event, handler)	# binds events
    after(ms, func)		    # calls a function after a delay
    update()			    # manually refresh the widget

    # Attributes used in Widgets
        # Text
            # text → Display text for Label, Button, Radiobutton, Checkbutton
            # image → Display image (PhotoImage or BitmapImage)
            # compound → Combines text and image (top, bottom, left, right, center)
            # justify → Align multi-line text (left, center, right)
            # wraplength → Wrap text after X pixels
        # Font
            # font → Font family, size, style (e.g., ("Arial", 12, "bold"))
            # fg → Foreground/text color
            # bg → Background color
            # highlightbackground → Border color when not focused
            # highlightcolor → Border color when focused
            # activeforeground → Text color when active 
            # activebackground → Background color when active
        # Dimensions & Placement
            # width → Width of widget (chars for Entry, pixels for Scale)
            # height → Height of widget (chars/lines for Label)
            # padx, pady → Padding inside geometry managers (pack, grid)
            # relief → Border style (flat, raised, sunken, groove, ridge)
            # bd → Border width
            # anchor → Position of content inside widget (n, s, e, w, center)
        # State & Interaction
            # state → Widget state: normal, disabled, active
            # command → Function executed on action
            # variable → Linked IntVar, StringVar, or FloatVar
            # value → Value of a Radiobutton when selected
            # onvalue / offvalue → Values for Checkbutton when checked/unchecked
            # show → Mask character for Entry (e.g., "*" for password)
            # validate → Input validation mode (focus, key, etc.)
            # validatecommand → Function executed for validation

# Widgets

    # Label
    widget = tk.Label(parent, text="", -attributes)	    # creates a text label
    # Attributes
        # text, image, compound, justify, wraplength, fg, bg, font, width, height, anchor, relief, bd

    
    # Button
    widget = tk.Button(parent, text="", command=function -attributes)	# creates a Button
    #Attributes
        #text, command, state, activeforeground, activebackground, fg, bg, font, width, height, relief, bd

    # Entry
    widget = tk.Entry(parent, -attributes)	        # creates a Text Entry Box
    # Attributes
        # width, show, textvariable, fg, bg, font, relief, bd, state

    # Option Box
    widget = ttk.Optionbox(parent, values = ["","",""], -attributes)    # creates a Dropdown Menu
    # Attributes
        # variable, values, fg, bg, font, width, height, relief, bd

    # Radio Button
    widget = tk.Radiobutton(parent, -attributes)	# creates a Radio Button
    # Attributes
        #text, variable, value, state, fg, bg, font, width, height, relief, bd

    # Check Button
    widget = tk.Checkbutton(parent, -attributes)	    #creates a Check Button
    # Attributes
        # text, variable, onvalue, offvalue, state, fg, bg, font, width, height, relief, bd

    # Spinbox
    widget = tk.Spinbox(parent, from_=0, to=10, incriment=1, -attributes)	# creates a Spinbox
    #Attributes
        #from_, to, increment, width, state, fg, bg, font, relief, bd, textvariable

    # Scale
    widget = tk.Scale(parent, from_=0, to=100, -attributes)		# creates a Scale Slider
    # Attributes
        # from_, to, orient, length, tickinterval, resolution, variable, showvalue, 
        # troughcolor, sliderlength, fg, bg, font, width, height, relief, bd
 
    # Example of a password Entry Box, showing only asterisks.
    password_entry = tk.Entry(root, show="*")

    # Example of a quit button
    exit_button = tk.Button(root, text="Exit", command=root.destroy)


