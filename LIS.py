import mysql.connector as con
import os
import datetime
import time
import re
import smtplib
import random
from tabulate import tabulate
path = con.connect(host = 'localhost', username = 'root', password = '@Hrishiadi200136', port = '3306')
db = path.cursor()
db.execute("USE LibraryInformationSystem;")



def Calculate_Fine():
    db.execute("Select User_No, SUM(Fine) from issue where S_No>0 group by User_No;")
    Fines=db.fetchall()
    for fine in Fines:
        fine=list(fine)
        if fine[0]:
            fine[0]=0
        db.execute("update Users set Fine = '{}' where Reg_ID = '{}';".format(fine[1],fine[0]))
        path.commit()
    

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


#MAIN MENU

##USER SIGNUP
def user_signup():
    db.execute("Select max(S_No) from Users")
    Max_S=db.fetchall()
    if Max_S[0][0]!=None:
        S_No=Max_S[0][0]+1
    else:
        S_No=1
    name=str(input("Name: "))
    rollno=str(input("Roll Number: "))
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
    BooksIssd=0
    fine=0
    print("""Membership Type -->
| 1 | Undergraduate Student |
| 2 | Postgraduate Student  |
| 3 | Research Scholar      |
| 4 | Faculty Member        |""")
    sel_Mem_Type=8
    while(sel_Mem_Type<0 or sel_Mem_Type>5):
        sel_Mem_Type=int(input("Enter Your Selection ==>"))
        if sel_Mem_Type == 1:
            Mem_Type='Undergrad Student'
        elif sel_Mem_Type == 2:
            Mem_Type='Postgrad Student'
        elif sel_Mem_Type == 3:
            Mem_Type='Research Scholar'
        elif sel_Mem_Type == 4:
            Mem_Type='Faculty Member'
        else:
            print("Invalid Entry")
    db.execute("select Reg_ID from Users")
    Reg_temp=db.fetchall()
    Reg_IDs=[]
    for i in Reg_temp:
        Reg_IDs.append(i[0])
    regno=random.randint(11111,99999)
    regid=Mem_Type[0]+str(S_No)+str(regno)
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
    db.execute("Insert Into Users(S_No, RollNo, Name, PhoneNo, Email, Password, User_type,  Reg_ID, RegDate, DOB , BooksIssd , Fine) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(S_No, rollno, name, phoneno, email, Pass2, Mem_Type, regid, RegDate,DOB, BooksIssd, fine))
    path.commit()



##LOGIN
def login():
    db.execute("select Reg_ID from Users;")
    ID_Temp=db.fetchall()
    IDs=[]
    for i in ID_Temp:
        IDs.append(i[0])
    db.execute("select Reg_ID from Admin;")
    ID_Temp=db.fetchall()
    for i in ID_Temp:
        IDs.append(i[0])
    ID = str(input("Enter Membership ID ==> "))
    pass2=str(input("Enter Password ==> "))
    pass1=''
    if ID in IDs:
        if ID[0]=='A':
            db.execute("select Password from Admin where Reg_ID = '{}';".format(ID))
            pass1=db.fetchall()[0][0]
        else:
            db.execute("select Password from Users where Reg_ID = '{}';".format(ID))
            pass1=db.fetchall()[0][0]
    else:
        return False
    if pass1!=pass2:
        print("Invalid Credentials")
        return False
    else:
        Ty=ID[0]
        return ID


## MAIN MENU(PAGE)
def main_menu():
    ans_main=0
    while(ans_main!=3):
        print("""
| 1 | Log In   |
| 2 | Register |
| 3 | Exit     |""")
        ans_main=int(input("Enter your Choice ==> "))
        if ans_main == 1:
            login_status = login()
            if login_status==False:
                continue
            else:
                return login_status
        elif ans_main == 2:
            user_signup()
            continue
        elif ans_main == 3:
            return False
    return True
        

#ADMIN PAGE

##ADMIN MENU
def admin_Menu(ID):
    ans_admin=0
    while(ans_admin!=4):
        print("""
| 1 | Veiw Users   |
| 2 | Veiw Books   |
| 3 | Veiw Profile |
| 4 | Logout       |
""")
        ans_admin=int(input("Enter your Choice ==> "))
        if ans_admin == 1:
            User_Ad_Menu()
        elif ans_admin == 2:
            BookUpdationMenu()
        elif ans_admin == 3:
            Profile_Admin(ID)
        
            
## VEIW Admin PROFILE
def Profile_Admin(ID):
    ans_prof=0
    while (ans_prof!=2):
        db.execute("Select Reg_ID, Name, PhoneNo, Email, DOB from Admin where Reg_ID='{}';".format(ID))
        profile_info=db.fetchall()[0]
        print("Admin ID: '{}'\nName: '{}'\nPhone No: '{}'\nEmail: '{}'\nDOB: '{}'\n".format(profile_info[0],profile_info[1],profile_info[2],profile_info[3],profile_info[4]))
        print("""SELECT
| 1 | Update |
| 2 | Return |
""")
        ans_prof=int(input("Enter your Selection ==> "))
        if ans_prof == 1:
            Update_Ad_Prof(ID)
        else:
            return

def Update_Ad_Prof(ID):
    PhoneNo = str(input("Enter Phone Number: "))
    Email=str(input("Enter Email ID: "))
    P_Code=0
    while P_Code==0:
        Pass1=str(input("Enter Your Password: "))
        Pass2=str(input("Re-Enter Your Password: "))
        if (Pass1 == Pass2):
            P_Code=1
        else:
            print("The Passwords do not Match\n\n\n")
    db.execute("Update Admin set PhoneNo='{}', Email='{}', Password='{}' where Reg_ID = '{}';".format(PhoneNo, Email, Pass2, ID))
    path.commit()
    
    

###User Details Menu
def User_Ad_Menu():
    User_Ad_choice=0
    while (User_Ad_choice !=4 ):
        Veiw_Users()
        print("""\n\n
| 1 | Add User       |
| 2 | Collect Fine   |
| 3 | Delete User    |
| 4 | Return to Main Menu |
""")
        User_Ad_choice=int(input("Enter your Choice ==> "))
        if User_Ad_choice == 1:
            ADD_User()
        elif User_Ad_choice == 2:
            Collect_Fine()
        elif User_Ad_choice == 3:
            Delete_User()
        elif User_Ad_choice == 4:
            return 0


    
####VEIW USERS
def Veiw_Users():
    db.execute("select S_No, RollNo, Name, PhoneNo, Email, Reg_ID, User_type, DOB, BooksIssd, Fine from Users")
    User_details=db.fetchall()
    print(tabulate(User_details,headers=['S_No','Roll Number','Name','Phone Number','Email','Membership ID','Membership Type','DOB','Books Issued','Fine']))
        
####ADD USER
def ADD_User():
    user_signup()

####Collect Fines
def Collect_Fine():
    Reg_ID=str(input("Enter the Membership ID of the User to Collect Fine ==> "))
    db.execute("select Fine from Users where Reg_ID = '{}';".format(Reg_ID))
    fine=db.fetchone()[0]
    Fine_co=str(input("Fine Collected (Y/N) ==> "))
    if Fine_co == 'Y' or Fine_co == 'y':
        db.execute("Update Users set Fine = 0 where Reg_ID = '{}';".format(Reg_ID))
        path.commit()
        db.execute("Update issue set Fine = 0 where Reg_ID = '{}';".format(Reg_ID))
        path.commit()


#### Delete User
def Delete_User():
    Reg_ID=str(input("Enter Membership ID of the user you want to Delete"))
    db.execute("Delete from Users where Reg_ID = '{}';".format(Reg_ID))
    path.commit()

    

###BOOK UPDATION

####ADD BOOK
def ADD_Book():
    db.execute("Select max(S_No) from Books")
    Max_S=db.fetchall()
    if Max_S[0][0]!=None:
        S_No=Max_S[0][0]+1
    else:
        S_No=1
    name=str(input("Book Name: "))
    Author=str(input("Author Name: "))
    Pub_Yr=int(input("Published Year: "))
    IBSN=str(input("Enter IBSN Number: "))
    copies=int(input("No of Copies: "))
    Avail=copies
    db.execute("Insert into Books(S_No, Name, Author, Pub_Yr, IBSN, No_Copies, Avail) values ('{}', '{}','{}', '{}', '{}', '{}', '{}');".format(S_No, name, Author, Pub_Yr, IBSN, copies,Avail))
    path.commit()


####UPDATE BOOK DETAILS
def Update_Book():
    IBSN=str(input("Enter the IBSN number of the book you want to update: "))
    db.execute("select No_Copies, Avail from Books where IBSN = '{}';".format(IBSN))
    B_info=db.fetchone()
    Bcopies, BAvail = B_info[0], B_info[1]
    name=str(input("Book Name: "))
    Author=str(input("Author Name: "))
    Pub_Yr=int(input("Published Year: "))
    issd=Bcopies-BAvail
    copies=int(input("No of Copies: "))
    while (copies<issd):
        copies=int(input("No of Copies: "))
        if (copies<issd):
            print("Invalid Entry")
            continue
    Avail=copies-issd
    db.execute("Update Books Set Name='{}', Author='{}', Pub_Yr='{}', No_Copies='{}', Avail='{}' where IBSN='{}';".format(name,Author,Pub_Yr,copies,Avail,IBSN))
    path.commit()


####Delete BOOK DETAILS
def Delete_Book():
    IBSN=str(input("Enter the IBSN number of the book you want to DELETE: "))
    db.execute("DELETE from Books where IBSN = '{}';".format(IBSN))
    path.commit()
    print("The Book with IBSN number '{}' is sucessfully deleted".format(IBSN))


####VEIW BOOK LIST
def Veiw_Books_Admin():
    db.execute("select S_No, Name, Author, Pub_Yr, IBSN, No_Copies, Avail from Books")
    Book_details=db.fetchall()
    print(tabulate(Book_details,headers=['S_No','Name','Author','Pub_Yr','IBSN','Total Copies','Available Copies']))


####VEIW BOOK ISSUE DETAILS
def Veiw_Issue_List():
    db.execute("select S_No, User_No, IBSN, IssueDate, ReturnDate, fine from issue")
    Issue_details=db.fetchall()
    print(tabulate(Issue_details,headers=['S_No','URN','IBSN','Issue Date','Return Date','Fine']))

###BOOK UPDATION MENU
def BookUpdationMenu():
    Veiw_Books_Admin()
    print("""SELECT
| 1 | Add Book            |
| 2 | Update Book         |
| 3 | Delete Book         |
| 4 | Veiw Issue Details  |
| 5 | Return to Main Menu |
""")
    ans_book=int(input("Enter Your Choice ==> "))
    if (ans_book==1):
        ADD_Book()
    elif (ans_book == 2):
        Update_Book()
    elif (ans_book == 3):
        Delete_Book()
    elif (ans_book==4):
        Veiw_Issue_List()
    elif (ans_book == 5):
        return false


#USER MENU

##BOOK MENU
####Book Limit
def book_limit(Ty):
    if Ty == 'U':
        return 2, 1
    elif Ty == 'P':
        return 4, 1
    elif Ty == 'R':
        return 6, 3
    elif Ty == 'F':
        return 10, 6


####VEIW BOOK LIST
def Veiw_Books_User():
    db.execute("select S_No, Name, Author, Pub_Yr, IBSN, No_Copies, Avail from Books where Avail>0;")
    Book_details=db.fetchall()
    print(tabulate(Book_details,headers=['S_No','Name','Author','Pub_Yr','IBSN','Total Copies','Available Copies']))
####Issue Book
def Issue_Book(ID):
    IBSN=str(input("Enter IBSN Number of the Book you want to Issue ==> "))
    db.execute("select sum(if(IBSN = '{}', 1, 0)) from issue where User_No = '{}' and ReturnDate is NULL;".format(IBSN, ID))
    ron=db.fetchall()[0][0]
    if ron==1:
        print("Book Already Issued!!\n\n")
        return
    db.execute("insert into issue(IBSN, User_No, IssueDate) values('{}','{}',CURDATE());".format(IBSN, ID))
    path.commit()
    db.execute("update Users set BooksIssd=BooksIssd+1 where Reg_ID = '{}';".format(ID))
    path.commit()
    db.execute("update Books set Avail=Avail-1 where IBSN = '{}';".format(IBSN))
    path.commit()


    
### Book Main Menu
def user_book_menu(ID):
    limit, duration = book_limit(ID[0])
    db.execute("select BooksIssd from Users where Reg_ID='{}';".format(ID))
    booksissd=db.fetchall()[0][0]
    limit_ans=0
    if booksissd>=limit:
        limit_ans=1
    ans_User_Book=0
    while (ans_User_Book!=2 and limit_ans==0):
        Veiw_Books_User()
        print("""SELECT
| 1 | Issue Book   |
| 2 | Back to Main |
""")
        ans_User_Book=int(input("Enter Your Selection ==> "))
        if ans_User_Book==1:
            Issue_Book(ID)
        else:
            print("Invalid Entry\n\n\n")
    else:
        Veiw_Books_User()
        print("Issue Limit Reached!!\n\n\n")

        
###User Issue Menu
def Veiw_User_Issue_List(ID):
    db.execute("select BooksIssd from Users where Reg_ID='{}';".format(ID))
    booksissd=db.fetchall()[0][0]
    if booksissd>0:
        db.execute("select IBSN, IssueDate, ReturnDate, fine from issue where User_No ='{}';".format(ID))
        Issue_details=db.fetchall()
        print(tabulate(Issue_details,headers=['IBSN','Issue Date','Return Date','Fine']))
    else:
        return 0

    
def Return_Book(ID):
    limit, duration = book_limit(ID[0])
    IBSN=str(input("Enter IBSN Number of the Book you want to Return ==> "))
    db.execute("select S_No from issue where (IBSN = '{}' and User_No = '{}') and ReturnDate is NULL;".format(IBSN,ID))
    S_No = db.fetchall()[0][0]
    db.execute("update issue set ReturnDate=CURDATE(), Fine = if(timestampdiff(month,CURDATE(), IssueDate)>'{}',timestampdiff(month,CURDATE(),IssueDate)*10,0) where S_No ='{}';".format(duration, S_No))
    path.commit()
    db.execute("update Users set BooksIssd=BooksIssd-1 where Reg_ID = '{}';".format(ID))
    path.commit()
    db.execute("update Books set Avail=Avail+1 where IBSN = '{}';".format(IBSN))
    path.commit()
    Calculate_Fine()

def user_issue_menu(ID):
    db.execute("select BooksIssd from Users where Reg_ID='{}';".format(ID))
    booksissd=db.fetchall()[0][0]
    limit_ans=0
    if booksissd<=0:
        limit_ans=1
    ans_issue_Book=0
    while (ans_issue_Book!=2 and limit_ans==0):
        Veiw_User_Issue_List(ID)
        print("""SELECT
| 1 | Return Book   |
| 2 | Back to Main |
""")
        ans_issue_Book=int(input("Enter Your Selection ==> "))
        if ans_issue_Book==1:
            Return_Book(ID)
            return
        elif(ans_issue_Book==2):
            return
        else:
            print("Invalid Entry\n\n\n")
    else:
        print("No Issued Books!!\n\n\n")



def Profile_User(ID):
    ans_prof=0
    while (ans_prof!=2):
        db.execute("Select Reg_ID, Name, PhoneNo, Email, DOB from Admin where Reg_ID='{}';".format(ID))
        profile_info=db.fetchall()[0]
        print("Admin ID: '{}'\nName: '{}'\nPhone No: '{}'\nEmail: '{}'\nDOB: '{}'\n".format(profile_info[0],profile_info[1],profile_info[2],profile_info[3],profile_info[4]))
        print("""SELECT
| 1 | Update |
| 2 | Return |
""")
        ans_prof=int(input("Enter your Selection ==> "))
        if ans_prof == 1:
            Update_Us_Prof(ID)
        else:
            return

def Update_Us_Prof(ID):
    PhoneNo = str(input("Enter Phone Number: "))
    Email=str(input("Enter Email ID: "))
    P_Code=0
    while P_Code==0:
        Pass1=str(input("Enter Your Password: "))
        Pass2=str(input("Re-Enter Your Password: "))
        if (Pass1 == Pass2):
            P_Code=1
        else:
            print("The Passwords do not Match\n\n\n")
    db.execute("Update Admin set PhoneNo='{}', Email='{}', Password='{}' where Reg_ID = '{}';".format(PhoneNo, Email, Pass2, ID))
    path.commit()
    


##USER MAIN MENU
def User_Menu(ID):
    ans_user=0
    while(ans_user!=4):
        print("""
| 1 | Veiw Books   |
| 2 | Veiw Issues  |
| 3 | Veiw Profile |
| 4 | Logout       |
""")
        ans_user=int(input("Enter your Choice ==> "))
        if ans_user == 1:
            user_book_menu(ID)
        elif ans_user == 2:
            user_issue_menu(ID)
        elif ans_user == 3:
            Profile_User(ID)





if __name__=="__main__":
    Calculate_Fine()
    main=True
    while (main!=False):
        main=main_menu()
        if main==False:
            break
        elif main[0]=='A':
            admin_Menu(main)
        elif main[0]=='U' or main[0]=='P' or main[0]=='R' or main[0] == 'F':
            User_Menu(main)
        
        
        
    
