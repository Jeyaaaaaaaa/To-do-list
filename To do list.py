import customtkinter as ctk
from tkcalendar import *
from datetime import *
import sqlite3
one_days=["January","March","May","July","August","October","December"]
two_days=["April","June","September","November"]
three_days=["February"]
day_is_all_right=False
month_is_all_right=False
year_is_all_right=False
month_has_31_days=False
month_has_30_days=False
month_has_28_days=False
conn=sqlite3.connect("CUSTOMER DETAILS.db")
c=conn.cursor()

class Reminders():
    row=4
    def __init__(self,day,month,data):
        self.day=day
        self.month=month
        self.data=data
        Reminders.row+=1
    def add_reminder_to_screen(self):
        self.output=ctk.CTkLabel(app,text=self.data)
        self.output1=ctk.CTkLabel(app,text=self.day)
        self.output2=ctk.CTkLabel(app,text=self.month)
        self.delete=ctk.CTkButton(app,text="Delete")
        self.delete.configure(command=lambda: self.delete_reminder())
        self.output1.grid(column=0,row=Reminders.row)
        self.output2.grid(column=1,row=Reminders.row)
        self.output.grid(column=2,row=Reminders.row)
        self.delete.grid(column=3,row=Reminders.row)
        self.add_to_database()
    def add_to_database(self):
        c.execute("INSERT INTO reminders VALUES (:day,:month,:reminder)",{'day': self.day,'month': self.month, 'reminder': self.data})
        conn.commit()
    
   

    def delete_reminder(self):
        self.output.destroy()
        self.output1.destroy()
        self.output2.destroy()
        self.delete.destroy()
    def delete_old_reminder(self):
        query="""DELETE FROM reminders WHERE day=:day AND month=:month AND reminder=:reminder"""
        c.execute(query,{'day': self.day,'month':self.month,'reminder': self.data})
        conn.commit()
        self.o.destroy()
        self.o1.destroy()
        self.o2.destroy()
        self.deletee.destroy()
        
        
        
    def add_old_reminder_to_screen(self):
        self.o=ctk.CTkLabel(app,text=self.data)
        self.o1=ctk.CTkLabel(app,text=self.day)
        self.o2=ctk.CTkLabel(app,text=self.month)
        self.deletee=ctk.CTkButton(app,text="Delete")
        self.deletee.configure(command=lambda: self.delete_old_reminder())
        self.o1.grid(column=0,row=Reminders.row)
        self.o2.grid(column=1,row=Reminders.row)
        self.o.grid(column=2,row=Reminders.row)
        self.deletee.grid(column=3,row=Reminders.row)
        
      




def check_months_one_days():
    global month_is_all_right
    global month_has_31_days
    temp=cal1.get()
    for i in range(0,len(one_days)):
        if one_days[i]==temp:
            month_is_all_right=True
            month_has_31_days=True
            break
    if month_is_all_right==False:
        check_months_two_days()
    else:
        check_days()
def check_months_two_days():
    global month_is_all_right
    global month_has_30_days
    temp=cal1.get()
    for i in range(0,len(two_days)):
        if two_days[i]==temp:
            month_is_all_right=True
            month_has_30_days=True
            break
    if month_is_all_right==False:
        check_months_three_days()
    else:
        check_days()
def check_months_three_days():
    global month_is_all_right
    global month_has_28_days
    temp=cal1.get()
    for i in range(0,len(three_days)):
        if three_days[i]==temp:
            month_is_all_right=True
            month_has_28_days=True
            break
    
    check_days()
def check_days():
    global day_is_all_right
    global month_has_31_days
    global month_has_30_days
    global month_has_28_days
    temp=cal.get()
    if temp.isdigit()==True:
        if int(temp)>=1 and int(temp)<=31 and month_has_31_days==True:
            day_is_all_right=True
        elif int(temp)>=1 and int(temp)<=30 and month_has_30_days==True:
            day_is_all_right=True
        elif int(temp)>=1 and int(temp)<=28 and month_has_28_days==True:
            day_is_all_right=True
        check_all_values()
        
def check_all_values():
    global day_is_all_right
    global month_is_all_right
    if month_is_all_right==True and day_is_all_right==True:
        item=Reminders(cal.get(),cal1.get(),reminder.get())
        item.add_reminder_to_screen()
        
    else:
        error_message=ctk.CTkLabel(app,text="Please input a valid month and date")
        error_message.grid(row=4,column=0)
        month_is_all_right=False

        
app=ctk.CTk()
reminder=ctk.CTkEntry(app,placeholder_text="Enter reminder")
reminder.grid(row=0,column=1)
cal=ctk.CTkEntry(app,placeholder_text="Enter a day")
cal1=ctk.CTkEntry(app,placeholder_text="Enter a month")
cal.grid(row=1,column=1)
cal1.grid(row=2,column=1)
confirmation=ctk.CTkButton(app,text="Add Reminder",command=check_months_one_days)
confirmation.grid(row=3,column=1)
c.execute("SELECT * FROM reminders")
for row in c:
    day=row[0]
    month=row[1]
    reminderrr=row[2]
    reminders=Reminders(day,month,reminderrr)
    reminders.add_old_reminder_to_screen() 
app.mainloop()
