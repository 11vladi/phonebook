import tkinter as tk
from tkinter import ttk, Menu, Frame
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, create_engine
from tkinter import messagebox as mbox
from contactEdit import ContactEdit
from sqlalchemy import update


Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)

class Book(tk.Tk):


    def loadDbData(self):
        s = Session(self.e)
        
        result = s.query(Contact).all()

        self.tree.delete(*self.tree.get_children())
        for row in result:
            self.tree.insert("", tk.END,iid=row.id, values=(
                row.firstname, row.lastname, row.phone))
        
    def __init__(self):

        super().__init__()
        self.title("Phone book")

        menubar = Menu(self)
        self.config(menu=menubar)
        
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)
        
        contactMenu = Menu(menubar)
        contactMenu.add_command(label="New contact", command=self.onNewContact)
        contactMenu.add_command(label="Change contact", command=self.onEditContact)
        contactMenu.add_command(label="Delete contact", command=self.onDeleteContact)
        menubar.add_cascade(label="Edit", menu=contactMenu)
   

        self.e = create_engine('sqlite:///bb.db', echo=True)
        #super().metadata.create_all(self.e) 
        Base.metadata.create_all(self.e)        

        

        columns = ("#1", "#2", "#3")
        self.tree = ttk.Treeview(self, show="headings", columns=columns)
       
        self.tree.heading("#1", text="first name")
        self.tree.heading("#2", text="last name")
        self.tree.heading("#3", text="Phone")
        ysb = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)

        self.loadDbData()

        self.tree.grid(row=0, column=0)
        ysb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def onEditContact(self):
        try:
            sel=self.tree.focus()[0]
            val=self.tree.item(sel)
           
            id=sel
            firstname=val.get("values")[0]
            lastname=val.get("values")[1]
            phone=str(val.get("values")[2])

            window = ContactEdit(self, firstname,lastname,phone)
            user = window.open()
            if user[0]==1:
                try:
                    self.updateContact(id,user[1],user[2],user[3])
                except:
                    mbox.showinfo(title=None, message="Error writing to datebase")
            self.loadDbData()
       
                                    
        except:
           mbox.showinfo(title=None, message="Select a contact")

    def onNewContact(self):
        window = ContactEdit(self, "","","")
        user = window.open()
        if user[0]==1:
            self.insert(user[1],user[2],user[3])
        self.loadDbData()

    def insert(self, firstname, lastname, phone):
        s = Session(self.e)
        c = Contact()
        c.firstname = firstname
        c.lastname = lastname
        c.phone = phone
        s.add(c)
        s.commit()

    def updateContact(self,id, afirstname, alastname, aphone):
        try:
         s = Session(self.e)
         s.execute(update(Contact).where(Contact.id == id).values(firstname=afirstname,lastname=alastname,phone=aphone))
         s.commit()
        except:
         mbox.showinfo(title=None, message="Error writing to database")  

        self.loadDbData()

    def onDeleteContact(self):
        try:
            sel=self.tree.focus()[0]
            val=self.tree.item(sel)
            print(val)
            answer = mbox.askokcancel("Question","you  want to delete a contact? "+(val.get("values")[0]+" "+val.get("values")[1]+" ?"))
            if answer==True:
                self.deleteContact(sel)
                self.loadDbData()
            
        except:
           mbox.showinfo(title=None, message=" Select a contact")     
       
    def deleteContact(self,id):
         s = Session(self.e)
         s.query(Contact).filter(Contact.id==id).delete()
         s.commit()

  

if __name__ == '__main__':
    app = Book()
    app.mainloop()
