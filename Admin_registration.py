import mysql.connector as con
import os
import datetime
import time
import re
import smtplib
import random
path = con.connect(host = 'localhost', username = 'root', password = '@Hrishiadi200136', port = '3306')
db = path.cursor()
db.execute("USE LibraryInformationSystem;")

#FETCH ALL PHONE NUMBERS
def fetch_phonenos():
    db.execute("select PhoneNo from Users;")
    P_temp=db.fetchall()
    Ph_Nos=[]
    for i in P_temp:
        Ph_Nos.append(i[0])
    db.execute("select PhoneNo from Admin;")
    P_temp=db.fetchall()
    for i in P_temp:
        Ph_Nos.append(i[0])
    return Ph_Nos

#FETCH ALL EMAILS
def fetch_emails():
    db.execute("select Email from Users;")
    E_temp=db.fetchall()
    Emails=[]
    for i in E_temp:
        Emails.append(i[0])
    db.execute("select Email from Admin;")
    E_temp=db.fetchall()
    for i in E_temp:
        Emails.append(i[0])
    return Emails



#ADMIN SIGNUP
def admin_signup():
    db.execute("Select max(S_No) from Admin")
    Max_S=db.fetchall()
    if Max_S[0][0]!=None:
        S_No=Max_S[0][0]+1
    else:
        S_No=1
    name=str(input("Name: "))
    p_val=True
    while(p_val):
        phoneno=str(input("Phone Number: "))
        p_nos=fetch_phonenos()
        if phoneno in p_nos:
            print("Phone Number Already Registered")
            break
        else :
            p_val = False
    e_val=True
    while (e_val):
        email=str(input("Email: "))
        email.lower()
        emails=fetch_emails()
        if email in emails:
            print("Email Already Registered")
            break
        else:
            e_val=False
    RegDate=datetime.date.today()
    yr=int(input("Year of Birth: "))
    mn=int(input("Month of Birth: "))
    dy=int(input("Day of Birth: "))
    DOB=datetime.date(yr, mn, dy)
    print("\n\n\n")
    db.execute("select Reg_ID from Users")
    Reg_temp=db.fetchall()
    Reg_IDs=[]
    for i in Reg_temp:
        Reg_IDs.append(i[0])
    regno=random.randint(11111,99999)
    regid='AD'+str(S_No)+str(regno)
    while regid in Reg_IDs:
        regno=random.randint(11111,99999)
        regid=Mem_Type[0]+str(S_No)+str(regno) 
    P_Code=0
    while P_Code==0:
        print("Your Membership ID is ", regid)
        Pass1=str(input("Enter Your Password ==> "))
        Pass2=str(input("Re-Enter Your Password ==> "))
        if (Pass1 == Pass2):
            P_Code=1
        else:
            print("The Passwords do not Match\n\n\n")
    db.execute("Insert Into Admin(S_No, Name, PhoneNo, Email, Password, Reg_ID, RegDate, DOB) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(S_No, name, phoneno, email, Pass2, regid, RegDate,DOB))
    path.commit()


if __name__=="__main__":
    admin_signup()
