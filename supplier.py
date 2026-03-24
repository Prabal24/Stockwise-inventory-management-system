from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

#Delete fun
def delete_supplier(invoice,treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error","No Row Is Selected")
        return
    cursor,connection= connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("DELETE FROM supplier_data WHERE invoice=%s",invoice)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo("Info","Record Is Deleted ")
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()

        #clear fun  
def clear(invoice_entry,name_entry,contact_entry,description_text,treeview):
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

#Search Fun

def search_supplier(search_value,treeview): 

 if search_value=="":
    messagebox.showerror("Error","Please Enter Innvoice No.")
 else:
    cursor,connection= connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("SELECT * from supplier_data WHERE invoice=%s",search_value)
        record=cursor.fetchone()
        if not record:
            messagebox.showerror("Error","No Record Found")
            return
        treeview.delete(*treeview.get_children())
        treeview.insert("",END,values=record)
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()    

        #Show_All

def show_all(treeview,search_entry):
     treeview_data(treeview) 
     search_entry.delete(0,END)  
 
              
        

#update function
def update_supplier(invoice,name,contact,description,treeview):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error","No Row Is Selected")
        return
    cursor,connection= connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("SELECT * from supplier_data WHERE invoice=%s",invoice)
        current_data=cursor.fetchone()
        current_data=current_data[1:]
        
        new_data=(name,contact,description)
        print(new_data)
        if current_data==new_data:
            messagebox.showinfo("Info","No Changes Detected")
            return

        cursor.execute("UPDATE supplier_data SET name=%s,contact=%s,description=%s WHERE invoice=%s",(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo("info","Data is Updated")
        treeview_data(treeview)
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close() 
            
    

def select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content["values"]
    invoice_entry.delete(0,END)
    name_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    invoice_entry.insert(0,actual_content[0])
    name_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])

def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
            return 
    try:
        cursor.execute("use inventory_system")
        cursor.execute("Select * from supplier_data")
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert("",END,values=record)
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close() 
                


def add_supplier(invoice,name,contact,description,treeview):
    if invoice=="" or name=="" or contact=="" or description.strip()=="":
        messagebox.showerror("Error","All fields are required")
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("SELECT * from supplier_data WHERE invoice=%s",invoice )
        if cursor.fetchone():
            messagebox.showerror("Error","Id Is Already Exists")
            return
        cursor.execute("CREATE TABLE IF NOT EXISTS supplier_data(invoice INT PRIMARY KEY, name VARCHAR(20),contact VARCHAR(10),description VARCHAR(30) )")
        cursor.execute("INSERT INTO supplier_data VALUES(%s,%s,%s,%s)",(invoice,name,contact,description.strip()))
        connection.commit()
        messagebox.showinfo("info","Data is inserted")
        treeview_data(treeview)
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close() 
        



def supplier_form(window):
    global back_image
    supplier_frame = Frame(window,width=1337,height=1067)
    supplier_frame.place(x=200,y=100)
    headingLable=Label(supplier_frame,text="Manage Supplier Details",font=("Times new roman",20,"bold"),bg="blue",fg="white")
    headingLable.place(x=0,y=0,relwidth=1)
    #Backbutton
    back_image=PhotoImage(file="back.png")
    back_button=Button(supplier_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:supplier_frame.place_forget())
    back_button.place(x=10,y=50)

    #LEFT FRAME
    left_frame=Frame(supplier_frame,bg="white")
    left_frame.place (x=20,y=150)

    invoice_label=Label(left_frame,text="Invoice No",font=("times new roman",15,"bold"),bg="white")
    invoice_label.grid(row=0,column=0,padx=(20,40),sticky="w")
    invoice_entry=Entry(left_frame,font=("times new roman",15,"bold"),bg="lightyellow")
    invoice_entry.grid(row=0,column=1)

    name_label=Label(left_frame,text="Supplier Name ",font=("times new roman",15,"bold"),bg="white")
    name_label.grid(row=1,column=0,padx=(20,40),pady=25,sticky="w")
    name_entry=Entry(left_frame,font=("times new roman",15,"bold"),bg="lightyellow")
    name_entry.grid(row=1,column=1)

    contact_label=Label(left_frame,text="Supplier Contact ",font=("times new roman",15,"bold"),bg="white")
    contact_label.grid(row=2,column=0,padx=(20,40),sticky="w")
    contact_entry=Entry(left_frame,font=("times new roman",15,"bold"),bg="lightyellow")
    contact_entry.grid(row=2,column=1)

    description_label=Label(left_frame,text="Description ",font=("times new roman",15,"bold"),bg="white")
    description_label.grid(row=3,column=0,padx=(20,40),sticky="nw",pady=25)
    description_text=Text(left_frame,width=40,heigh=20,bd=4,bg="lightyellow")
    description_text.grid(row=3,column=1,pady=25)
    
    #Buttons

    button_frame=Frame(left_frame)
    button_frame.grid(row=4,columnspan=2,pady=20)
#Add
    add_button=Button(button_frame ,text="Add",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:add_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)

#Update
    update_button=Button(button_frame ,text="Update",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:update_supplier(invoice_entry.get(),name_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    update_button.grid(row=0,column=1,padx=20)
    
    #DELETE
    delete_button=Button(button_frame ,text="Delete",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0,column=2,padx=20)

    #Clear
    clear_button=Button(button_frame ,text="Clear",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:clear(invoice_entry,name_entry,contact_entry,description_text,treeview))
    clear_button.grid(row=0,column=3,padx=20)

    #Right Frame
    right_frame=Frame(supplier_frame,bg="White")
    right_frame.place(x=735,y=150,width=600,height=500)

    search_frame=Frame(right_frame,bg="White")
    search_frame.pack(pady=10)

    num_label=Label(search_frame,text="Invoice No",font=("times new roman",15,"bold"),bg="white")
    num_label.grid(row=0,column=0,padx=20,sticky="w")
    search_entry=Entry(search_frame,font=("times new roman",15,"bold"),bg="lightyellow",width=12)
    search_entry.grid(row=0,column=1)

    search_button=Button(search_frame ,text="Search",font=("Times New Roman",15,"bold"),cursor="hand2",width=10,fg="white",bg="blue",command=lambda:search_supplier(search_entry.get(),treeview))
    search_button.grid(row=0,column=2,padx=20)

    show_button=Button(search_frame ,text="Show ALL",font=("Times New Roman",15,"bold"),cursor="hand2",width=10,fg="white",bg="blue",command=lambda:show_all(treeview,search_entry))
    show_button.grid(row=0,column=3,padx=20)


    scrolly = Scrollbar(right_frame, orient=VERTICAL)
    scrollx = Scrollbar(right_frame, orient=HORIZONTAL)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))


    treeview = ttk.Treeview(
    right_frame,
    columns=("invoice", "name", "contact", "description"),
    show="headings",
    yscrollcommand=scrolly.set,
    xscrollcommand=scrollx.set
)

    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading("invoice", text="Invoice Id")
    treeview.heading("name", text="Supplier Name")
    treeview.heading("contact", text="Supplier Contact")
    treeview.heading("description", text="Description")

    treeview.column("invoice",width=90)
    treeview.column("name",width=160)
    treeview.column("contact",width=130)
    treeview.column("description",width=300)


    treeview_data(treeview)
    treeview.bind("<ButtonRelease-1>",lambda event:select_data(event,invoice_entry,name_entry,contact_entry,description_text,treeview))

    return supplier_frame