import random 
import tkinter as tk 
from tkinter import * 
from tkinter import messagebox 

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Name(Base):
    __tablename__ = 'some_table'
    id = Column(Integer, primary_key=True)
    firstname =  Column(String(50))
    lastname =  Column(String(50))

engine = create_engine('sqlite:///pythonsqlite.db')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

# create a Session
session = Session()

main_menu = tk.Tk()

firstname_label = Label(main_menu, text="First name")

# First name get 
firstname_entry = tk.StringVar()
firstname_entry_entry = Entry(main_menu, textvariable=firstname_entry)
firstname_label.grid(row=0, column=0)
firstname_entry_entry.grid(row=1, column=0)

# Second name get 
secondname_entry = tk.StringVar()
secondname_entry_entry = Entry(main_menu, textvariable=secondname_entry)
secondname_label = Label(main_menu, text="Second name")

secondname_label.grid(row=2, column=0)
secondname_entry_entry.grid(row=3, column=0)

def savedata(): 
    myobject = Name(firstname=firstname_entry.get(), lastname=secondname_entry.get())
    session.add(myobject)
    session.commit()

def show_table():
    names = session.query(Name).all()
    print(names)
    start = 7
    for idx,name in enumerate(names): 
        fname = Entry(main_menu)
        fname.grid(row=start+idx, column=0)
        fname.insert(END, name.firstname)
        lname = Entry(main_menu)
        lname.insert(END, name.lastname)
        lname.grid(row=start+idx, column=1)

def drop_rows():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


Button(text="Enter",command=savedata).grid(row=4, column=0)
Button(text="Show data",command=show_table).grid(row=5, column=0)
Button(text="Drop data",command=drop_rows).grid(row=6, column=0)

main_menu.mainloop()
