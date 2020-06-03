from tkinter import *
import pandas as pd
from tkinter import messagebox
from PIL import Image, ImageTk


def take_attendance(win, date, division, username):

    def go_back():
        R5.destroy()
        main_window(date, division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("700x700+300+100")
    R5.resizable(height=False, width=False)
    Button(R5, text='Go Back', command=lambda: go_back()).place(x=200, y=100)

    R5.mainloop()


def edit(win, date, division, username):

    df = pd.read_csv("{}.csv".format(division))

    def check_details():
        if day_var.get() != 'Day' and month_var.get() != 'Month' and year_var.get() != 'Year' and attendance.get() != 'N/A' and roll_no.get() != 0:
            req_date = day_var.get() + " " + month_var.get() + ", " + year_var.get()
            edit_attendance(req_date, attendance.get(), roll_no.get())
        else:
            messagebox.showerror("Error", "Enter data correctly")

    def edit_attendance(req_date, req_remark, req_roll_no):
        if req_roll_no in df['Roll No.'].to_numpy():
            if req_date in df.columns:
                df.set_index('Roll No.', inplace=True)
                df.loc[req_roll_no][req_date] = attendance.get()
                df.reset_index(inplace=True)
                df.to_csv("{}.csv".format(division), index=False)
                messagebox.showinfo("Info", "Attendance changed successfully")
            else:
                messagebox.showerror("Error", "No Record")
        else:
            messagebox.showerror("Error", "Roll no. is incorrect")


    def go_back():
        R5.destroy()
        main_window(date, division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("400x400+300+100")
    R5.resizable(height=False, width=False)
    roll_no = IntVar()
    roll_no.set(0)
    Button(R5, text='Go Back', command=lambda: go_back()).place(x=160, y=280)
    Label(R5, text='Enter Roll no.', font=("Times", 20, 'italic')).place(x=100, y=10)
    Entry(R5, textvariable=roll_no).place(x=100, y=50)

    day_list = [str(i) for i in range(1, 32)]
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    year_list = ['2019', '2020', '2021']

    day_var = StringVar()
    month_var = StringVar()
    year_var = StringVar()
    day_var.set("Day")
    month_var.set("Month")
    year_var.set("Year")

    Label(R5, text='Enter Date', font=("Times", 20, 'italic')).place(x=100, y=80)

    day_menu = OptionMenu(R5, day_var, *day_list).place(x=100, y=120)
    month_menu = OptionMenu(R5, month_var, *month_list).place(x=170, y=120)
    year_menu = OptionMenu(R5, year_var, *year_list).place(x=260, y=120)

    attendance = StringVar()
    Label(R5, text='Attendance', font=("Times", 20, 'italic')).place(x=100, y=165)
    OptionMenu(R5, attendance, 'A', 'P').place(x=250, y=165)
    attendance.set("N/A")
    Button(R5, text='Edit Attendance', command=check_details).place(x=130, y=220)

    R5.mainloop()


def report(win, date, division, username):

    def go_back():
        R5.destroy()
        main_window(date, division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("700x700+300+100")
    R5.resizable(height=False, width=False)
    Button(R5, text='Go Back', command=lambda: go_back()).place(x=200, y=100)

    R5.mainloop()


def view_data(req_date, division, win, curr_date, username):

    df = pd.read_csv("{}.csv".format(division))
    df_columns = df.columns
    def go_back():
        view(R6, curr_date, division, username)

    win.destroy()
    R6 = Tk()
    R6.geometry("700x600+300+100")
    R6.resizable(height=False, width=False)
    container = Frame(R6)
    canvas = Canvas(container, height=500, width=470)
    scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)
    scrollable_frame = Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    if req_date not in df.columns:
        Label(R6, text='No record', font=("Times", 50)).place(x=200, y=175)
    else:
        Label(scrollable_frame, text='Roll No.', font=("Times", 20, 'bold')).grid(row=0, column=0)
        Label(scrollable_frame, text='Name of Student', font=("Times", 20, 'bold')).grid(row=0, column=1)
        Label(scrollable_frame, text='Attendance', font=("Times", 20, 'bold')).grid(row=0, column=2)
        j=3
        for roll, name, remark in zip(df['Roll No.'], df['Name of Student'], df[req_date]):
            Label(scrollable_frame, text=roll).grid(row=j, column=0)
            Label(scrollable_frame, text=name).grid(row=j, column=1)
            Label(scrollable_frame, text=remark).grid(row=j, column=2)
            j += 1

    Button(R6, text='Go Back', command=go_back).place(x=600, y=20)
    Label(R6, text=division).place(x=600, y=60)
    Label(R6, text=req_date).place(x=600, y=110)
    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    R6.mainloop()

def view(win, date, division, username):


    def check_date():
        if day_var.get() != 'Day' and month_var.get() != 'Month' and year_var.get() != 'Year':
            view_data(day_var.get()+" "+month_var.get()+", "+year_var.get(), division, R5, date, username)
        else:
            messagebox.showerror("Error", "Enter date correctly")

    def go_back():
        R5.destroy()
        main_window(date, division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("300x300+300+10")
    R5.resizable(height=False, width=False)
    day_list = [str(i) for i in range(1, 32)]
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    year_list = ['2019', '2020', '2021']

    day_var = StringVar()
    month_var = StringVar()
    year_var = StringVar()
    day_var.set("Day")
    month_var.set("Month")
    year_var.set("Year")

    day_menu = OptionMenu(R5, day_var, *day_list).place(x=70, y=20)
    month_menu = OptionMenu(R5, month_var, *month_list).place(x=140, y=20)
    year_menu = OptionMenu(R5, year_var, *year_list).place(x=230, y=20)



    Button(R5, text='Go Back', command=lambda: go_back()).place(x=30, y=80)

    Button(R5, text="View Attendance", command=check_date).place(x=120, y=80)


    R5.mainloop()


def main_window(date, division, username):

    def logout(win):
        win.destroy()
        login()

    def go_back(win):
        win.destroy()
        select_window(username)

    R4 = Tk()
    R4.geometry("600x600+300+100")
    R4.resizable(height=False, width=False)
    image = Image.open("background.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(R4, image=photo).pack()

    new_attend_img = ImageTk.PhotoImage(Image.open("new.PNG"))
    edit_img = ImageTk.PhotoImage(Image.open("edit.PNG"))
    report_img = ImageTk.PhotoImage(Image.open("report.PNG"))
    view_img = ImageTk.PhotoImage(Image.open("view.PNG"))

    Button(R4, image=new_attend_img, bd=0, command=lambda: take_attendance(R4, date, division, username)).place(x=160, y=180, width=280)
    Button(R4, image=edit_img, bd=0, command=lambda: edit(R4, date, division, username)).place(x=160, y=270, width=280)
    Button(R4, image=report_img, bd=0, command=lambda: report(R4, date, division, username)).place(x=160, y=360, width=280)
    Button(R4, image=view_img, bd=0, command=lambda: view(R4, date, division, username)).place(x=160, y=450, width=280)

    Label(R4, text='Date: {}'.format(date), font=("Times", 14)).place(x=50, y=40)
    Label(R4, text='Class: {}'.format(division), font=("Times", 14)).place(x=50, y=80)
    Label(R4, text='Username: {}'.format(username), font=("Times", 16)).place(x=50, y=120)
    logout_button = Button(R4, text='Logout', font=("Times", 12), command=lambda: logout(R4)).place(x=500, y=40)
    go_back_button = Button(R4, text='Go back', font=("Times", 12), command=lambda: go_back(R4)).place(x=400, y=40)

    R4.mainloop()


def select_window(username):

    def destroy_win(win):
        win.destroy()
        login()

    def check_date_class(day, month, year, div):
        if day.get() != 'Day' and month.get() != 'Month' and year.get() != 'Year' and div.get() != 'Class':
            goto_next_win()
        else:
            messagebox.showerror("Error", "Please enter date and class correctly")

    def goto_next_win():
        R3.destroy()
        main_window(day_var.get()+" "+month_var.get()+", "+year_var.get(), class_var.get(), username)

    R3 = Tk()
    R3.geometry("400x400+300+100")
    R3.resizable(height=False, width=False)
    image = Image.open("mainwindow.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(R3, image=photo, height=600, width=600).pack()
    logout = Button(R3, text='Logout', font=("Times", 13), width=10, command=lambda: destroy_win(R3)).place(x=250, y=20)

    Label(R3, text="User: {}".format(username), font=("Times", 13)).place(x=30, y=340)

    day_list = [str(i) for i in range(1, 32)]
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    year_list = ['2019', '2020', '2021']

    day_var = StringVar()
    month_var = StringVar()
    year_var = StringVar()
    day_var.set("Day")
    month_var.set("Month")
    year_var.set("Year")

    day_menu = OptionMenu(R3, day_var, *day_list).place(x=70, y=150)
    month_menu = OptionMenu(R3, month_var, *month_list).place(x=140, y=150)
    year_menu = OptionMenu(R3, year_var, *year_list).place(x=230, y=150)

    class_list = ['8A', '8B', '9A', '9B', '10A', '10B']
    class_label = Label(R3, text='Select Class', font=("Times", 12)).place(x=70, y=200)
    class_var = StringVar()
    class_var.set("Class")
    class_menu = OptionMenu(R3, class_var, *class_list).place(x=180, y=200)

    submit_button = Button(R3, text='Submit', font=("Times", 12), command=lambda: check_date_class(day_var, month_var, year_var, class_var)).place(x=70, y=250)
    R3.mainloop()


def login():
    global root
    root = Tk()
    root.geometry("400x400+300+100")
    root.resizable(height=False, width=False)
    image = Image.open("loginpage.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(root, image=photo, height=400, width=400).pack()
    def check_login():
        Users = pd.read_csv("users.csv")
        if username_var.get() in Users['Username'].to_numpy():
            if password_var.get() == Users[Users['Username'] == username_var.get()]['Password'].to_numpy():
                root.destroy()
                select_window(username_var.get())
            else:
                messagebox.showerror("Error", "Incorrect Password")
        else:
            messagebox.showerror("Error", "Incorrect Username")


    username_label = Label(root, text='Username', font=('bold', 20)).place(x=30, y=100)
    username_var = StringVar()
    username_entry = Entry(root, textvariable=username_var, width=30, font=('Times', 10)).place(x=180, y=112)

    password_label = Label(root, text='Password', font=('bold', 20)).place(x=30, y=150)
    password_var = StringVar()
    password_entry = Entry(root, textvariable=password_var, width=30, font=('Times', 10), show="*").place(x=180, y=162)

    submit_button = Button(root, text='Submit', font=('Times', 13), command=check_login).place(x=170, y=200)
    signup_button = Button(root, text='Sign Up', font=('Times', 13), command=sign_up).place(x=167, y=245)
    root.mainloop()

def sign_up():

    def destroy_win(win):
        win.destroy()
        login()

    def check_signup():
        Users = pd.read_csv("users.csv")
        if username_var.get() in Users['Username'].to_numpy():
            messagebox.showerror("Error", "Username taken")
        else:
            if password_var.get() == confirm_password_var.get():
                temp = {'Username': username_var.get(), 'Password': password_var.get()}
                Users = Users.append(temp, ignore_index=True)
                Users.to_csv("Users.csv", index=False)
                R2.destroy()
                select_window(username_var.get())
            else:
                messagebox.showerror("Error", "Password do not match")

    global root
    root.destroy()
    R2 = Tk()
    R2.geometry("400x400+300+100")
    R2.resizable(height=False, width=False)
    image = Image.open("loginpage.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(R2, image=photo, height=400, width=400).pack()
    username_label = Label(R2, text='Username', font=('bold', 20)).place(x=30, y=100)
    username_var = StringVar()
    username_entry = Entry(R2, textvariable=username_var, width=30, font=('Times', 10)).place(x=180, y=112)

    password_label = Label(R2, text='Password', font=('bold', 20)).place(x=30, y=150)
    password_var = StringVar()
    password_entry = Entry(R2, textvariable=password_var, width=30, font=('Times', 10), show="*").place(x=180, y=162)

    confirm_password_label = Label(R2, text='Confirm', font=('bold', 20)).place(x=30, y=200)
    confirm_password_var = StringVar()
    confirm_password_entry = Entry(R2, textvariable=confirm_password_var, width=30, font=("Times", 10), show="*").place(x=180, y=212)

    submit_button = Button(R2, text='Submit', font=('Times', 13), command=check_signup).place(x=110, y=262)
    go_back_button = Button(R2, text='Go back', font=('Times', 13), command=lambda: destroy_win(R2)).place(x=230, y=262)
    R2.mainloop()

login()

