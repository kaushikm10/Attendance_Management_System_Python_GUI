from tkinter import *
import pandas as pd
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime

def take_attendance(win, division, username):

    def go_back():
        root.destroy()
        main_window(division, username)

    df=pd.read_csv("{}.csv".format(division))

    rows=df.shape[0]
    vars=[]
    today=datetime.now()
    date = str(int(today.strftime("%d")))+" "+today.strftime("%B")+", "+today.strftime("%Y")
    def setAttendance():
        for i in range(rows):
            df.loc[i, date]=vars[i].get()

    def logout(win):
        win.destroy()
        login()

    win.destroy()
    root = Tk()
    root.geometry("600x600+0+0")
    root['bg']='#efee9d'

    Button(root, text='Go Back',font=("Times", 12),bg='#ffcb74', command=go_back).place(x=40, y=520)
    logout_button = Button(root, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(root)).place(x=500, y=520)
    container = Frame(root,bg='#efee9d')
    canvas = Canvas(container,height=500, width=470,bg='#efee9d')
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview,bg='#efee9d')
    scrollable_frame = Frame(canvas,bg='#efee9d')

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    Label(scrollable_frame, text='Roll No.', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=0)
    Label(scrollable_frame, text='Name of Student', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=1)
    Label(scrollable_frame, text='Attendance', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=2)
    j=3

    for i in range(rows):

        Label(scrollable_frame, text=df.loc[i, 'Roll No.'],bg='#efee9d').grid(row=j, column=0)
        Label(scrollable_frame, text=df.loc[i, 'Name of Student'],bg='#efee9d').grid(row=j, column=1)
        l = ('A', 'P')
        var = StringVar()
        om = OptionMenu(scrollable_frame, var, *l)
        om.config(indicatoron=0, compound=RIGHT,bg='#ffcb74')
        var.set("P")
        om.grid(row=j, column=2)
        vars.append(var)
        j += 1

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    submit_button = Button(root, text='Submit', font=("Times", 12),bg='#ffcb74', command=setAttendance).place(x=280,y=520)
    root.mainloop()
    df.to_csv("{}.csv".format(division),index=False)


def edit(win, division, username):

    df = pd.read_csv("{}.csv".format(division))

    def logout(win):
        win.destroy()
        login()

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
        main_window( division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("600x600+0+0")
    R5.resizable(height=False, width=False)
    R5['bg']='#efee9d'
    roll_no = IntVar()
    roll_no.set(0)

    Button(R5, text='Go Back',font=("Times", 12),bg='#ffcb74', command=lambda: go_back()).place(x=40, y=40)
    logout_button = Button(R5, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(R5)).place(x=500, y=40)

    Label(R5, text='Enter Roll no.', font=("Times", 20, 'italic'),bg='#efee9d').place(x=200, y=160)
    Entry(R5, textvariable=roll_no).place(x=200, y=200)

    day_list = [str(i) for i in range(1, 32)]
    month_list = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    year_list = ['2019', '2020', '2021']

    day_var = StringVar()
    month_var = StringVar()
    year_var = StringVar()
    day_var.set("Day")
    month_var.set("Month")
    year_var.set("Year")

    Label(R5, text='Enter Date', font=("Times", 20, 'italic'),bg='#efee9d').place(x=200, y=230)

    day_menu = OptionMenu(R5, day_var, *day_list)
    day_menu.place(x=200, y=270)
    day_menu.config(bg='#ffcb74')

    month_menu = OptionMenu(R5, month_var, *month_list)
    month_menu.place(x=270, y=270)
    month_menu.config(bg='#ffcb74')

    year_menu = OptionMenu(R5, year_var, *year_list)
    year_menu.place(x=360, y=270)
    year_menu.config(bg='#ffcb74')

    attendance = StringVar()
    Label(R5, text='Attendance', font=("Times", 20, 'italic'),bg='#efee9d').place(x=200, y=315)
    om=OptionMenu(R5, attendance, 'A', 'P')
    om.place(x=350, y=230)
    om.config(bg='#ffcb74')
    attendance.set("P")
    Button(R5, text='Edit Attendance',bg='#ffcb74', command=check_details).place(x=230, y=370)

    R5.mainloop()


def report(win,division, username):

    df = pd.read_csv("{}.csv".format(division))

    def logout(win):
        win.destroy()
        login()

    def go_back():
        report.destroy()
        main_window(division, username)

    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    year_list = ['2019', '2020', '2021']

    win.destroy()
    report = Tk()
    report.geometry("600x600+0+0")
    report.resizable(height=False, width=False)
    report['bg']='#efee9d'

    Button(report, text='Go Back',font=("Times", 12),bg='#ffcb74', command=lambda: go_back()).place(x=40, y=40)
    logout_button = Button(report, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(report)).place(x=500, y=40)

    def check_date():
        if month_var.get() != 'Month' and year_var.get() != 'Year':
            col=[]
            present=0
            absent=0
            dt=month_var.get()+", "+year_var.get()
            for i in df.columns:
                if(dt in i):
                    col.append(i)
                    present=present+df[i].value_counts()['P']
                    absent=absent+df[i].value_counts()['A']
            if len(col)==0:
                messagebox.showerror("Error", "No data for this month exists.")
            else:
                def genearte():
                    df1=df[['Name of Student','Roll No.']+col]
                    for c in col:
                        df1[c] = df1[c].map({"A":0, "P":1})
                    df1['Percentage'] = df1[col].sum(axis=1)*100/len(col)
                    for c in col:
                        df1[c] = df1[c].map({0:"A", 1:"P"})
                    df1.to_csv('Reports/'+month_var.get()+year_var.get()+'.csv')
                    messagebox.showinfo("Info", "File saved in Reports folder")
                per=str(round(present/(present+absent)*100,2))+"%"
                Label(report, text='Month :', font=("Times", 20),bg='#efee9d').place(x=170,y=250)
                Label(report, text=dt, font=("Times",20),bg='#efee9d').place(x=270,y=250)
                Label(report, text='Attendance:', font=("Times",20),bg='#efee9d').place(x=130,y=300)
                Label(report, text=per, font=("Times",20),bg="#efee9d").place(x=270,y=300)
                Button(report, text='Generate Sheet', font=("Times", 20),bg='#ffcb74',command=genearte).place(x=200,y=400)
        else:
            messagebox.showerror("Error", "Enter month and year correctly")

    month_var = StringVar()
    year_var = StringVar()
    month_var.set('Month')
    year_var.set('Year')
    month_menu = OptionMenu(report, month_var, *month_list)
    month_menu.place(x=220, y=140)
    month_menu.config(bg='#ffcb74')
    year_menu = OptionMenu(report, year_var, *year_list)
    year_menu.place(x=310, y=140)
    year_menu.config(bg='#ffcb74')
    submit_button = Button(report, text='Submit', font=("Times", 12),bg='#ffcb74',command=check_date).place(x=260, y=200)
    report.mainloop()

def view_data(req_date, division, win, username):

    df = pd.read_csv("{}.csv".format(division))
    df_columns = df.columns
    def go_back():
        view(R6, division, username)

    def logout(win):
        win.destroy()
        login()

    win.destroy()
    R6 = Tk()
    R6.geometry("600x600+0+0")
    R6.resizable(height=False, width=False)
    R6['bg']='#efee9d'

    container = Frame(R6,bg='#efee9d')
    canvas = Canvas(container, height=500, width=470,bg='#efee9d')
    scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview,bg='#efee9d')
    scrollable_frame = Frame(canvas,bg='#efee9d')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    if req_date not in df.columns:
        Label(R6, text='No record', font=("Times", 50),bg='#efee9d').place(x=200, y=175)
    else:
        Label(scrollable_frame, text='Roll No.', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=0)
        Label(scrollable_frame, text='Name of Student', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=1)
        Label(scrollable_frame, text='Attendance', font=("Times", 20, 'bold'),bg='#efee9d').grid(row=0, column=2)
        j=3
        for roll, name, remark in zip(df['Roll No.'], df['Name of Student'], df[req_date]):
            Label(scrollable_frame, text=roll,bg='#efee9d').grid(row=j, column=0)
            Label(scrollable_frame, text=name,bg='#efee9d').grid(row=j, column=1)
            Label(scrollable_frame, text=remark,bg='#efee9d').grid(row=j, column=2)
            j += 1

    Button(R6, text='Go Back',font=("Times", 12),bg='#ffcb74', command=go_back).place(x=40, y=520)
    logout_button = Button(R6, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(R6)).place(x=500, y=520)

    Label(R6, text=division,bg='#efee9d').place(x=280, y=520)
    Label(R6, text=req_date,bg='#efee9d').place(x=260, y=550)
    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    R6.mainloop()

def view(win, division, username):
    today=datetime.now()
    date = str(int(today.strftime("%d")))+" "+today.strftime("%B")+", "+today.strftime("%Y")

    def logout(win):
        win.destroy()
        login()

    def check_date():
        if day_var.get() != 'Day' and month_var.get() != 'Month' and year_var.get() != 'Year':
            view_data(day_var.get()+" "+month_var.get()+", "+year_var.get(), division, R5, username)
        else:
            messagebox.showerror("Error", "Enter date correctly")

    def go_back():
        R5.destroy()
        main_window(division, username)

    win.destroy()
    R5 = Tk()
    R5.geometry("600x600+0+0")
    R5.resizable(height=False, width=False)
    R5['bg']='#efee9d'
    day_list = [str(i) for i in range(1, 32)]
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    year_list = ['2019', '2020', '2021']

    day_var = StringVar()
    month_var = StringVar()
    year_var = StringVar()
    day_var.set("Day")
    month_var.set("Month")
    year_var.set("Year")

    logout_button = Button(R5, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(R5)).place(x=500, y=40)

    day_menu = OptionMenu(R5, day_var, *day_list)
    day_menu.place(x=170, y=220)
    day_menu.config(bg='#ffcb74')
    month_menu = OptionMenu(R5, month_var, *month_list)
    month_menu.place(x=240, y=220)
    month_menu.config(bg='#ffcb74')
    year_menu = OptionMenu(R5, year_var, *year_list)
    year_menu.place(x=330, y=220)
    year_menu.config(bg='#ffcb74')



    Button(R5, text='Go Back',font=("Times", 12),bg='#ffcb74', command=lambda: go_back()).place(x=40, y=40)

    Button(R5, text="View Attendance",font=("Times", 12),bg='#ffcb74', command=check_date).place(x=220, y=280)


    R5.mainloop()


def main_window(division, username):
    today=datetime.now()
    date = str(int(today.strftime("%d")))+" "+today.strftime("%B")+", "+today.strftime("%Y")
    def logout(win):
        win.destroy()
        login()

    def go_back(win):
        win.destroy()
        select_window(username)

    R4 = Tk()
    R4.geometry("600x600+0+0")
    R4.resizable(height=False, width=False)
    R4['bg'] = '#efee9d'

    # image = Image.open("background.jpg")
    # photo = ImageTk.PhotoImage(image)
    # Label(R4, image=photo).pack()

    # new_attend_img = ImageTk.PhotoImage(Image.open("new.PNG"))
    # edit_img = ImageTk.PhotoImage(Image.open("edit.PNG"))
    # report_img = ImageTk.PhotoImage(Image.open("report.PNG"))
    # view_img = ImageTk.PhotoImage(Image.open("view.PNG"))

    Button(R4, bg="#ffcb74", text="Take Attendance", fg="#000",font=("Helvetica", 24, 'italic'), bd=4, command=lambda: take_attendance(R4, division, username)).place(x=160, y=180, width=280, height=80)
    Button(R4, bg="#ffcb74", text="Edit Attendance", fg="#000",font=("Helvetica", 24, 'italic'), bd=4, command=lambda: edit(R4, division, username)).place(x=160, y=270, width=280, height=80)
    Button(R4, bg="#ffcb74", text="Report", bd=4, fg="#000",font=("Helvetica", 24, 'italic'), command=lambda: report(R4, division, username)).place(x=160, y=360, width=280, height=80)
    Button(R4, bg="#ffcb74", text="View", bd=4, fg="#000", font=("Helvetica", 24, 'italic'), command=lambda: view(R4, division, username)).place(x=160, y=450, width=280, height=80)

    Label(R4, text='Date: {}'.format(date), font=("Times", 14),bg='#efee9d').place(x=50, y=40)
    Label(R4, text='Class: {}'.format(division), font=("Times", 14),bg='#efee9d').place(x=50, y=80)
    Label(R4, text='Username: {}'.format(username), font=("Times", 16),bg='#efee9d').place(x=50, y=120)
    logout_button = Button(R4, text='Logout', font=("Times", 12),bg='#ffcb74', command=lambda: logout(R4)).place(x=500, y=40)
    go_back_button = Button(R4, text='Go back', font=("Times", 12),bg='#ffcb74', command=lambda: go_back(R4)).place(x=400, y=40)

    R4.mainloop()


def select_window(username):

    def destroy_win(win):
        win.destroy()
        login()

    def check_date_class(div):
        if div.get() != 'Class':
            goto_next_win()
        else:
            messagebox.showerror("Error", "Please select a class")

    def goto_next_win():
        R3.destroy()
        main_window(class_var.get(), username)

    R3 = Tk()
    R3.geometry("600x600+0+0")
    R3.resizable(height=False, width=False)
    R3['bg'] = '#efee9d'
    # image = Image.open("mainwindow.jpg")
    # photo = ImageTk.PhotoImage(image)
    # Label(R3, image=photo, height=600, width=600).pack()
    logout = Button(R3, text='Logout', font=("Times", 13),bg='#ffcb74', width=10, command=lambda: destroy_win(R3)).place(x=450, y=20)

    Label(R3, text="User: {}".format(username), font=("Times", 13),bg='#efee9d').place(x=50, y=550)


    class_list = ['8A', '8B', '9A', '9B', '10A', '10B']
    class_label = Label(R3, text='Select Class', font=("Times", 12),bg='#efee9d').place(x=200, y=300)
    class_var = StringVar()
    class_var.set("Class")
    class_menu = OptionMenu(R3, class_var, *class_list)
    class_menu.place(x=300, y=300)
    class_menu.config(bg='#ffcb74')
    submit_button = Button(R3, text='Submit', font=("Times", 12),bg='#ffcb74', command=lambda: check_date_class(class_var)).place(x=270, y=350)
    R3.mainloop()


def login():
    global root
    root = Tk()
    root.geometry("600x600+0+0")
    root.resizable(height=False, width=False)
    root['bg'] = '#efee9d'
    # image = Image.open("loginpage.jpg")
    # photo = ImageTk.PhotoImage(image)
    # Label(root, image=photo, height=400, width=400).pack()
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


    username_label = Label(root, text='Username', font=('bold', 20),bg='#efee9d').place(x=120, y=200)
    username_var = StringVar()
    username_entry = Entry(root, textvariable=username_var, width=30, font=('Times', 10)).place(x=270, y=212)

    password_label = Label(root, text='Password', font=('bold', 20),bg='#efee9d').place(x=120, y=250)
    password_var = StringVar()
    password_entry = Entry(root, textvariable=password_var, width=30, font=('Times', 10), show="*").place(x=270, y=262)

    submit_button = Button(root, text='Submit', font=('Times', 13),bg='#ffcb74', command=check_login).place(x=267, y=300)
    signup_button = Button(root, text='Sign Up', font=('Times', 13),bg='#ffcb74', command=sign_up).place(x=267, y=345)
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
    R2.geometry("600x600+0+0")
    R2.resizable(height=False, width=False)
    R2['bg'] = '#efee9d'
    # image = Image.open("loginpage.jpg")
    # photo = ImageTk.PhotoImage(image)
    # Label(R2, image=photo, height=400, width=400).pack()
    username_label = Label(R2, text='Username', font=('bold', 20),bg='#efee9d').place(x=120, y=200)
    username_var = StringVar()
    username_entry = Entry(R2, textvariable=username_var, width=30, font=('Times', 10)).place(x=270, y=212)

    password_label = Label(R2, text='Password', font=('bold', 20),bg='#efee9d').place(x=120, y=250)
    password_var = StringVar()
    password_entry = Entry(R2, textvariable=password_var, width=30, font=('Times', 10), show="*").place(x=270, y=262)

    confirm_password_label = Label(R2, text='Confirm', font=('bold', 20),bg='#efee9d').place(x=120, y=300)
    confirm_password_var = StringVar()
    confirm_password_entry = Entry(R2, textvariable=confirm_password_var, width=30, font=("Times", 10), show="*").place(x=270, y=312)

    submit_button = Button(R2, text='Submit', font=('Times', 13),bg='#ffcb74', command=check_signup).place(x=200, y=362)
    go_back_button = Button(R2, text='Go back', font=('Times', 13),bg='#ffcb74', command=lambda: destroy_win(R2)).place(x=320, y=362)
    R2.mainloop()

login()
