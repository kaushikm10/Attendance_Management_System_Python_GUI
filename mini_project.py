from tkinter import *
import pandas as pd
from tkinter import messagebox
from PIL import Image, ImageTk


def main_window(date, division):

    def logout(win):
        win.destroy()
        login()

    R4 = Tk()
    R4.geometry("600x600")
    R4.resizable(height=False, width=False)
    image = Image.open("background.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(R4, image=photo).pack()
    Label(R4, text='View', font=('Times', 20)).place(x=150, y=150)
    Label(R4, text='Report', font=('Times', 20)).place(x=150, y=450)
    Label(R4, text='New', font=('Times', 20)).place(x=450, y=150)
    Label(R4, text='Date: {}'.format(date), font=("Times", 14)).place(x=50, y=50)
    Label(R4, text='Class: {}'.format(division), font=("Times", 14)).place(x=50, y=120)

    logout_button = Button(R4, text='Logout', font=("Times", 12), command=lambda: logout(R4)).place(x=500, y=50)

    R4.mainloop()


def select_window():

    def destroy_win(win):
        win.destroy()
        login()

    def goto_next_win(win):
        win.destroy()
        main_window(day_var.get()+" "+month_var.get()+", "+year_var.get(), class_var.get())

    R3 = Tk()
    R3.geometry("400x400")
    R3.resizable(height=False, width=False)
    image = Image.open("mainwindow.jpg")
    photo = ImageTk.PhotoImage(image)
    Label(R3, image=photo, height=600, width=600).pack()
    logout = Button(R3, text='Logout', font=("Times", 13), width=10, command=lambda: destroy_win(R3)).place(x=250, y=20)

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
    class_menu = OptionMenu(R3, class_var, *class_list).place(x=180, y=200)

    submit_button = Button(R3, text='Submit', font=("Times", 12), command=lambda: goto_next_win(R3)).place(x=150, y=300)
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
                select_window()
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
                select_window()
            else:
                messagebox.showerror("Error", "Password do not match")

    global root
    root.destroy()
    R2 = Tk()
    R2.geometry("400x400")
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

