'''
In this assignment, you will create a database named student_info.db that holds the following information about students at a college:
The student’s name
The student’s major
The department in which the student is enrolled
The database should have the following tables:

Majors table
MajorID: INTEGER PRIMARY KEY
Name: Text

Departments table
DeptID INTEGER PRIMARY KEY
Name TEXT

Students table
StudentID: INTEGER PRIMARY KEY
Name: TEXT
MajorID: INTEGER Foreign Key
DeptID: INTEGER Foreign Key

Write a program that creates the database and the tables.

Write a program that performs CRUD operations on the Majors table. Specifically, the program should allow the user to do the following:
___ Add a new major
___ Search for an existing major
___ Update an existing major
___ Delete an existing major
___ Show a list of all majors

Write a program that performs CRUD operations on the Departments table. Specifically, the program should allow the user to do the following:
___ Add a new department
___ Search for an existing department
___ Update an existing department
___ Delete an existing department
___ Show a list of all departments

Write a program that performs CRUD operations on the Students table. Specifically, the program should allow the user to do the following:
___ Add a new student
___ Search for an existing student
___ Update an existing student
___ Delete an existing student
___ Show a list of all students
When adding, updating, and deleting rows, be sure to enable foreign key enforcement. When adding a new student to the Students table, the user should only be allowed to select an existing major from the Departments table, and an existing department from the Departments table.
'''

import tkinter as tk
from tkinter import messagebox
from db_functions import get_departments, get_majors, get_students, get_dept_id, get_major_id, get_student_id, add_major, update_major, search_major, delete_major, list_majors, add_department, update_department, search_department, delete_department, list_departments, add_student, search_student, update_student, delete_student, list_students

### Create the GUI
root = tk.Tk()
root.title("Student Major Database")
root.geometry("700x500+600+400")

databaseList = ("Major", "Department", "Student")
database = tk.StringVar()
database.set("")

menuList =()
menu = tk.StringVar()

# Create Frames to use
dbFrame = tk.Frame(root)
dbFrame.pack(pady=10)
menuFrame = tk.Frame(root)
menuFrame.pack(pady=10)
mainFrame = tk.Frame(root)
mainFrame.pack(pady=10)

# Creates the Database Selection Frame
dbLabel = tk.Label(dbFrame, text="Select a Database: ")
dbLabel.grid(column=0, row=0)
dbEntry = tk.OptionMenu(dbFrame, database, *databaseList, command=lambda _: db_change())
dbEntry.grid(column=1, row=0)

# Emptys a frame in the GUI to be re-populated with the new menu items
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def db_change(*args):
    entry = database.get()
    clear_frame(menuFrame)
    clear_frame(mainFrame)
    if entry == "Major":
        db_major()
    elif entry == "Department":
        db_department()
    elif entry == "Student":
        db_student()

## For the Major Database
def db_major():
    # Sets the Menu Variables
    menuList = ("Add a new major", "Search for an existing major", "Update an existing major", "Delete an existing major", "Show a list of all majors")
    menu.set("")

    #Creates the Menu Frame
    majorLabel = tk.Label(menuFrame, text="Select an Operation: ")
    majorLabel.grid(column=0, row=0)
    majorMenu = tk.OptionMenu(menuFrame, menu, *menuList, command=lambda _: menu_change())
    majorMenu.grid(column=1, row=0)

    def menu_change():
        entry = menu.get()
        majorName = tk.StringVar()
        majorID = tk.IntVar()
        majors = get_majors()
        majorName.set("")
        major1 = tk.StringVar()
        major1.set(majors[0])

        if entry == menuList[0]: # Add a new Major
            clear_frame(mainFrame) # Clear the Main Frame

            # Select the name of the new major
            majorLabel = tk.Label(mainFrame, text="Enter the name of the new Major")
            majorLabel.grid(column=0, row=0)
            majorEntry = tk.Entry(mainFrame, textvariable=majorName)
            majorEntry.grid(column=1, row=0)

            def submit():
                major = majorName.get()
                if major == "":
                    messagebox.showinfo("Failure!", "You did not enter a major to add.")
                    return
                result = add_major(major)
                if result == True:
                    messagebox.showinfo("Success!", f"Added {major} to available majors.")
                elif result == False:
                    messagebox.showinfo("Failure!", "That major already exists, try again.")

            # Submit button
            submitButton = tk.Button(mainFrame, text="Submit", command=submit)
            submitButton.grid(row=2, column=0, columnspan=2)
            
            
        elif entry == menuList[1]: # Search for a Major
            clear_frame(mainFrame)
            majorID.set(None)
            majorIDString = tk.StringVar()
            majorIDString.set(f"Enter a Major to search for.")

            # Enter a Major to Search For
            majorLabel = tk.Label(mainFrame, text="Enter the Major you are searching for: ")
            majorLabel.grid(column=0, row=0)
            majorEntry = tk.Entry(mainFrame, textvariable=majorName)
            majorEntry.grid(column=1, row=0)

            # Show the Major ID resulting from that major
            idLabel = tk.Label(mainFrame, textvariable=majorIDString)
            idLabel.grid(column=0, row=1, columnspan=2)
            
            def submit():
                major = majorName.get()
                if search_major(major) == None:
                    majorIDString.set("That Major does not exist.")
                else:
                    majorIDString.set(f"The Major ID is: {search_major(major)}")

            # Submit aButtons
            submitButton = tk.Button(mainFrame, text="Submit", command = submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[2]: # Update a Major
            clear_frame(mainFrame)
            newMajor = tk.StringVar()

            # Select an old Major to edit
            oldLabel = tk.Label(mainFrame, text="Select the Major you want to change:")
            oldSelect = tk.OptionMenu(mainFrame, major1, *majors)
            oldLabel.grid(column=0, row=0)
            oldSelect.grid(column=1, row=0)

            # Rename the Major
            newLabel = tk.Label(mainFrame, text="Enter the new name for the Major:")
            newSelect = tk.Entry(mainFrame, textvariable=newMajor)
            newLabel.grid(column=0, row=1)
            newSelect.grid(column=1, row=1)

            def submit():
                nMajor = newMajor.get()
                oMajor = major1.get()
                result = update_major(oMajor, nMajor)
                if result == False:
                    messagebox.showinfo("Failure!", f"The major {oMajor} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The major {oMajor} has been updated to {nMajor}.")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=2, columnspan=2)


        elif entry == menuList[3]: # Delete a Major
            clear_frame(mainFrame)

            # Select an old Major to edit
            delLabel = tk.Label(mainFrame, text="Select the Major you want to delete:")
            delSelect = tk.OptionMenu(mainFrame, major1, *majors)
            delLabel.grid(column=0, row=0)
            delSelect.grid(column=1, row=0)

            def submit():
                major = major1.get()
                result = delete_major(major)
                if result == False:
                    messagebox.showinfo("Failure!", f"The major {major} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The major {major} has been removed.")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[4]: # Show all Majors
            clear_frame(mainFrame)
            majorDict = list_majors()
            majorListString = tk.StringVar()
            
            output = f"{'Major ID':<10}  {'Major Name'}\n"
            output += "-" * 40 + "\n"
            for major_id, name in majorDict.items():
                output += f"{major_id:<10}  {name}\n"
            majorListString.set(output)

            tk.Label(mainFrame, textvariable=majorListString, justify="left", font=("courier")).pack()

            

## For the Department Database
def db_department():
     # Sets the Menu Variables
    menuList = ("Add a new department", "Search for an existing department", "Update an existing department", "Delete an existing department", "Show a list of all departments")
    menu.set("")

    #Creates the Menu Frame
    majorLabel = tk.Label(menuFrame, text="Select an Operation: ")
    majorLabel.grid(column=0, row=0)
    majorMenu = tk.OptionMenu(menuFrame, menu, *menuList, command=lambda _:menu_change())
    majorMenu.grid(column=1, row=0)

    def menu_change():
        entry = menu.get()
        deptName = tk.StringVar()
        deptID = tk.IntVar()
        depts = get_departments()
        deptName.set("")
        dept1 = tk.StringVar()
        dept1.set(depts[0])

        if entry == menuList[0]: # Add a new Department
            clear_frame(mainFrame) # Clear the Main Frame

            # Select the name of the new department
            deptLabel = tk.Label(mainFrame, text="Enter the name of the new Department")
            deptLabel.grid(column=0, row=0)
            deptEntry = tk.Entry(mainFrame, textvariable=deptName)
            deptEntry.grid(column=1, row=0)

            def submit():
                dept = deptName.get()
                if dept == "":
                    messagebox.showinfo("Failure!", "You did not enter a department to add.")
                    return
                result = add_department(dept)
                if result == True:
                    messagebox.showinfo("Success!", f"Added {dept} to available department.")
                elif result == False:
                    messagebox.showinfo("Failure!", "That department already exists, try again.")

            # Submit button
            submitButton = tk.Button(mainFrame, text="Submit", command=submit)
            submitButton.grid(row=2, column=0, columnspan=2)
            
            
        elif entry == menuList[1]: # Search for a Department
            clear_frame(mainFrame)
            deptID.set(None)
            deptIDString = tk.StringVar()
            deptIDString.set(f"Enter a department to search for.")

            # Enter a Major to Search For
            deptLabel = tk.Label(mainFrame, text="Enter the department you are searching for: ")
            deptLabel.grid(column=0, row=0)
            deptEntry = tk.Entry(mainFrame, textvariable=deptName)
            deptEntry.grid(column=1, row=0)

            # Show the Major ID resulting from that major
            idLabel = tk.Label(mainFrame, textvariable=deptIDString)
            idLabel.grid(column=0, row=1, columnspan=2)
            
            def submit():
                dept = deptName.get()
                if search_department(dept) == None:
                    deptIDString.set("That department does not exist.")
                else:
                    deptIDString.set(f"The department ID is: {search_department(dept)}")

            # Submit aButtons
            submitButton = tk.Button(mainFrame, text="Submit", command = submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[2]: # Update a Department
            clear_frame(mainFrame)
            newDept = tk.StringVar()

            # Select an old Major to edit
            oldLabel = tk.Label(mainFrame, text="Select the department you want to change:")
            oldSelect = tk.OptionMenu(mainFrame, dept1, *depts)
            oldLabel.grid(column=0, row=0)
            oldSelect.grid(column=1, row=0)

            # Rename the Major
            newLabel = tk.Label(mainFrame, text="Enter the new name for the department:")
            newSelect = tk.Entry(mainFrame, textvariable=newDept)
            newLabel.grid(column=0, row=1)
            newSelect.grid(column=1, row=1)

            def submit():
                nDept = newDept.get()
                oDept = dept1.get()
                result = update_department(oDept, nDept)
                if result == False:
                    messagebox.showinfo("Failure!", f"The department {oDept} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The department {oDept} has been updated to {nDept}.")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=2, columnspan=2)


        elif entry == menuList[3]: # Delete a Department
            clear_frame(mainFrame)

            # Select an old Major to edit
            delLabel = tk.Label(mainFrame, text="Select the department you want to delete:")
            delSelect = tk.OptionMenu(mainFrame, dept1, *depts)
            delLabel.grid(column=0, row=0)
            delSelect.grid(column=1, row=0)

            def submit():
                dept = dept1.get()
                result = delete_department(dept)
                if result == False:
                    messagebox.showinfo("Failure!", f"The department {dept} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The department {dept} has been removed.")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[4]: # Show all Departments
            clear_frame(mainFrame)
            deptDict = list_departments()
            deptListString = tk.StringVar()
            
            output = f"{'Dept ID':<10}  {'Department Name'}\n"
            output += "-" * 40 + "\n"
            for dept_id, name in deptDict.items():
                output += f"{dept_id:<10}  {name}\n"
            deptListString.set(output)

            tk.Label(mainFrame, textvariable=deptListString, justify="left", font=("courier")).pack()

## For the Student Database
def db_student():
    # Sets the Menu Variables
    menuList = ("Add a new student", "Search for an existing student", "Update an existing student", "Delete an existing student", "Show a list of all students")
    menu.set("")

    #Creates the Menu Frame
    studentLabel = tk.Label(menuFrame, text="Select an Operation: ")
    studentLabel.grid(column=0, row=0)
    studentMenu = tk.OptionMenu(menuFrame, menu, *menuList, command=lambda _:menu_change())
    studentMenu.grid(column=1, row=0)

    def menu_change():
        entry = menu.get()
        studentName = tk.StringVar()
        studentID = tk.IntVar()
        students = get_students()
        studentName.set("")
        stud1 = tk.StringVar()
        stud1.set(students[0])
        depts = get_departments()
        majors = get_majors()
        deptName = tk.StringVar()
        majorName = tk.StringVar()
        deptName.set("")
        majorName.set("")

        if entry == menuList[0]: # Add a new Student
            clear_frame(mainFrame) # Clear the Main Frame

            # Select the name of the new student
            nameLabel = tk.Label(mainFrame, text="Enter the name of the new Student")
            nameLabel.grid(column=0, row=0)
            nameEntry = tk.Entry(mainFrame, textvariable=studentName)
            nameEntry.grid(column=1, row=0)
            majorLabel = tk.Label(mainFrame, text="Select the Student's Major: ")
            majorLabel.grid(column=0, row=1)
            majorEntry = tk.OptionMenu(mainFrame, majorName, *majors)
            majorEntry.grid(column=1, row=1)
            deptLabel = tk.Label(mainFrame, text="Select the Student's Department: ")
            deptLabel.grid(column=0, row=2)
            deptEntry = tk.OptionMenu(mainFrame, deptName, *depts)
            deptEntry.grid(column=1, row=2)

            def submit():
                stud = studentName.get()
                major = majorName.get()
                dept = deptName.get()
                majorID = get_major_id(major)
                deptID = get_dept_id(dept)
                
                if stud == "":
                    messagebox.showinfo("Failure!", "You did not enter a student to add.")
                    return
                
                if major == "":
                    major = "N/A"
                if dept == "":
                    dept = "N/A"
                
                result = add_student(stud, majorID, deptID)
                if result == True:
                    messagebox.showinfo("Success!", f"Added {stud} with a major of {major} in the {dept} department.")
                elif result == False:
                    messagebox.showinfo("Failure!", "That student already exists.")

            # Submit button
            submitButton = tk.Button(mainFrame, text="Submit", command=submit)
            submitButton.grid(row=3, column=0, columnspan=2)
                      
        elif entry == menuList[1]: # Search for a Student
            clear_frame(mainFrame)
            studentID.set(None)
            studIDString = tk.StringVar()
            studIDString.set(f"Enter a student to search for.")

            # Enter a Student to Search For
            studLabel = tk.Label(mainFrame, text="Enter the student you are searching for: ")
            studLabel.grid(column=0, row=0)
            studEntry = tk.Entry(mainFrame, textvariable=studentName)
            studEntry.grid(column=1, row=0)

            # Show the Student ID, Major, and Deptartment resulting from that student
            idLabel = tk.Label(mainFrame, textvariable=studIDString)
            idLabel.grid(column=0, row=1, columnspan=2)
            
            def submit():
                student = studentName.get()
                student_info = search_student(student)
                if student_info:
                    studID = student_info["StudentID"]
                    major = student_info["Major"]
                    dept = student_info["Department"]
                    studIDString.set(f"ID: {studID}\nName: {student}\nMajor: {major}\nDepartment: {dept}")
                else:
                    studIDString.set(f"Error: Student '{student}' not found.")

            # Submit aButtons
            submitButton = tk.Button(mainFrame, text="Submit", command = submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[2]: # Update a Student
            clear_frame(mainFrame)
            newStudID = tk.IntVar()
            newStud = tk.StringVar()

            # Select a Student to edit
            oldLabel = tk.Label(mainFrame, text="Select the student you want to change:")
            oldSelect = tk.OptionMenu(mainFrame, studentName, *students, command=lambda _: change_student())
            oldLabel.grid(column=0, row=0)
            oldSelect.grid(column=1, row=0)

            def change_student():
                student = studentName.get()
                student_info = search_student(student)
                deptName.set(student_info["Department"])
                majorName.set(student_info["Major"])
                newStud.set(student)
                newStudID.set(student_info["StudentID"])

            # Change the Student Name
            newStudLabel = tk.Label(mainFrame, text="Enter the new name for the student: ")
            newStudEntry = tk.Entry(mainFrame, textvariable=newStud)
            newStudLabel.grid(column=0, row=1)
            newStudEntry.grid(column=1, row=1)

            # Change the Student Major
            newMajorLabel = tk.Label(mainFrame, text="Select a new major (keep for no change):")
            newMajorLabel.grid(column=0, row=2)
            newMajorSelect = tk.OptionMenu(mainFrame, majorName, *majors)
            newMajorSelect.grid(column=1, row=2)

            # Change the Student Department
            newDeptLabel = tk.Label(mainFrame, text="Select a new department (keep for no change):")
            newDeptLabel.grid(column=0, row=3)
            newDeptSelect = tk.OptionMenu(mainFrame, deptName, *depts)
            newDeptSelect.grid(column=1, row=3)


            def submit():
                oStudent = studentName.get()
                nStudent = newStud.get()
                major = majorName.get()
                dept = deptName.get()
                studentInfo = search_student(oStudent)
                oMajor = studentInfo["Major"]
                oDept = studentInfo["Department"]
                
                if oMajor == major:
                    major = None
                if oDept == dept:
                    dept = None
                if nStudent == oStudent:
                    nStudent = None
                
                studID = get_student_id(oStudent)
                majorID = get_major_id(major)
                deptID = get_dept_id(dept)

                if majorID is None and deptID is None and nStudent is None:
                    messagebox.showinfo("Failure!", f"No Changes were made.")
                    return
                result = update_student(studID, nStudent, majorID, deptID)                   
                if result == False:
                    messagebox.showinfo("Failure!", f"The student {oStudent} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The {oStudent} has been updated:\nStudent ID: {studID}\nName: {nStudent}\nMajor: {major}\n Department: {dept}")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=4, columnspan=2)

        elif entry == menuList[3]: # Delete a Student
            clear_frame(mainFrame)

            # Select an old Student to edit
            delLabel = tk.Label(mainFrame, text="Select the student you want to delete:")
            delSelect = tk.OptionMenu(mainFrame, studentName, *students)
            delLabel.grid(column=0, row=0)
            delSelect.grid(column=1, row=0)

            def submit():
                student = studentName.get()
                studID = get_student_id(student)
                result = delete_student(studID)
                if result == False:
                    messagebox.showinfo("Failure!", f"The student {student} does not exist.")
                else:
                    messagebox.showinfo("Success!", f"The student {student} has been removed.")
                    menu_change()

            # Adds a Submit Button
            submitButton = tk.Button(mainFrame, text="Sumbit", command=submit)
            submitButton.grid(column=0, row=2, columnspan=2)

        elif entry == menuList[4]: # Show all Students
            clear_frame(mainFrame)
            studList = list_students()
            studListString = tk.StringVar()
            
            output = f"{'Student ID':<10}  {'Student Name':<25} {'Major':<20} {'Department':<20}\n"
            output += "-" * 75 + "\n"
            for student_id, name, major, dept in studList:
                output += f"{student_id:<10}  {name:<25}  {major or 'N/A':<20}  {dept or 'N/A':<20}\n"

            studListString.set(output)

            tk.Label(mainFrame, textvariable=studListString, justify="left", font=("courier")).pack()


root.mainloop()