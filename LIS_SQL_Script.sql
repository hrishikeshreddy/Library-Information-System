Create Database LibraryInformationSystem;
USE LibraryInformationSystem;
create table Users(S_No int not null, RollNo varchar(50) not null, Name varchar(50) not null, PhoneNo varchar(15) not null, Email varchar(50) not null, Password varchar(50) not null, User_type varchar(50) not null,  Reg_ID varchar(50) not null, RegDate Date not null, DOB date not null, BooksIssd int not null, Fine int, Primary Key(Reg_ID));
create table Admin(S_No int not null, Name varchar(50) not null, PhoneNo varchar(15) null, Email varchar(50) not null, Password varchar(50) not null,  Reg_ID varchar(50) not null, RegDate Date not null, DOB date not null, Primary Key(Reg_ID));
create table Books(S_No int not null, Name varchar(50) not null, Author varchar(50) not null, Pub_Yr year not null, IBSN varchar(50) not null, No_Copies int not null, Avail int not null,Primary Key(IBSN));
create table issue(S_No int not null auto_increment, IBSN varchar(50) not null, User_No varchar(50) not null, foreign key(IBSN) REFERENCES Books(IBSN), foreign key(User_No) REFERENCES Users(Reg_ID), IssueDate Date not null, ReturnDate date, fine int, primary key(S_NO));

drop table Admin;

select * from Users;
Delete from 

