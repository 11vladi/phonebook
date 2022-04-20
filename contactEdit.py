
import tkinter  as tk 


class ContactEdit(tk.Toplevel):

    def __init__(self,parent, fname,lname,phone): 
        super().__init__(parent)

        self.fname = tk.StringVar()
        self.lname = tk.StringVar()
        self.phone = tk.StringVar()
        self.result=0

        label = tk.Label(self, text="Edit contact ") 
        e_fname = tk.Entry(self, textvariable=self.fname)
        e_lname = tk.Entry(self, textvariable=self.lname)
        e_phone = tk.Entry(self, textvariable=self.phone)

        e_fname.delete(0,"end")
        e_fname.insert(0,fname)

        e_lname.delete(0,"end")
        e_lname.insert(0,lname)

        e_phone.delete(0,"end")
        e_phone.insert(0,phone)

        btnOk = tk.Button(self, text="OK", command=self.closeOK)
        btnCancel = tk.Button(self, text="Cancel", command=self.destroy)

        label.grid(row=0, columnspan=2)
        tk.Label(self, text="first name:").grid(row=1, column=0)
        tk.Label(self, text="last name:").grid(row=2, column=0)
        tk.Label(self, text="phone:").grid(row=3, column=0)
        e_fname.grid(row=1, column=1)
        e_lname.grid(row=2, column=1)
        e_phone.grid(row=3, column=1)
        btnOk.grid(row=4, columnspan=1)
        btnCancel.grid(row=4, columnspan=3)
    def closeOK(self):
        self.result=1
        self.destroy()

    def open(self):
        self.grab_set()
        self.wait_window()
        fname= self.fname.get()
        lname=self.lname.get()
        phone = self.phone.get()
        res=self.result
        return res,fname,lname,phone   
        
       


   