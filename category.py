from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from employees import connect_database

def select_data(event,id_entry,category_name_entry,description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content=content["values"]
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)
    id_entry.insert(0,actual_content[0])
    category_name_entry.insert(0,actual_content[1])
    description_text.insert(1.0,actual_content[2])
    

def clear(id_entry,category_name_entry,description_text,treeview):
    id_entry.delete(0,END)
    category_name_entry.delete(0,END)
    description_text.delete(1.0,END)

def delete_category(treeview):
    index = treeview.selection()
    content=treeview.item(index)
    row=content["values"]
    id=row[0]
    if not index:
        messagebox.showerror("Error","No Row Is Selected")
        return
    cursor,connection= connect_database()
    if not cursor or not connection:
            return
    try:
        cursor.execute("use inventory_system")
        cursor.execute("DELETE FROM category_data WHERE id=%s",id)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo("Info","Record Is Deleted ")
    except Exception as e:
     messagebox.showerror("Error",f"Error due to {e}")
    finally:
        cursor.close()
        connection.close()



def treeview_data(treeview):
    
        cursor,connection=connect_database()
        if not cursor or not connection:
                return 
        try:    
            cursor.execute("use inventory_system")
            cursor.execute("Select * from category_data")
            records=cursor.fetchall()
            treeview.delete(*treeview.get_children())
            for record in records:
                treeview.insert("",END,values=record)
        except Exception as e:
         messagebox.showerror("Error",f"Error due to {e}")
        finally:
         cursor.close()
         connection.close()        
    

def add_category(id,name,description,treeview):
    if id=="" or name=="" or description=="":
       messagebox.showerror("Error","All fields are required")
    else:
        cursor,connection = connect_database()
        if not cursor or not connection:
            return
        try:    
            cursor.execute("use inventory_system")
            cursor.execute("CREATE TABLE IF NOT EXISTS category_data(id INT PRIMARY KEY, name VARCHAR(100),description VARCHAR(300) )")
            cursor.execute("SELECT * from category_data WHERE id=%s",id )
            if cursor.fetchone():
                messagebox.showerror("Error","Id Is Already Exists")
                return
            cursor.execute("INSERT INTO category_data VALUES(%s,%s,%s)",(id,name,description))
            connection.commit()
            messagebox.showinfo("info","Data is inserted")
            treeview_data(treeview)
        except Exception as e:
         messagebox.showerror("Error",f"Error due to {e}")
        finally:
         cursor.close()
         connection.close()     


    
def category_form(window):
    global back_image,logo
    category_frame = Frame(window,width=1337,height=1067)
    category_frame.place(x=200,y=100)
    headingLable=Label(category_frame,text="Manage Category Details",font=("Times new roman",20,"bold"),bg="blue",fg="white")
    headingLable.place(x=0,y=0,relwidth=1)
    back_image=PhotoImage(file="back.png")
    back_button=Button(category_frame,image=back_image,bd=0,cursor="hand2",bg="white",command=lambda:category_frame.place_forget())
    back_button.place(x=10,y=50)

    logo = PhotoImage(file="features.png")
    label=Label(category_frame,image=logo)
    label.place(x=50,y=100)

    details_frame=Frame(category_frame)
    details_frame.place(x=800,y=80)

    id_label=Label(details_frame,text="Id.",font=("times new roman",15,"bold"),bg="white")
    id_label.grid(row=0,column=0,padx=(20),sticky="w")
    id_entry=Entry(details_frame,font=("times new roman",15,"bold"),bg="lightyellow")
    id_entry.grid(row=0,column=1)

    category_name_lable=Label(details_frame,text="Category Name",font=("times new roman",15,"bold"),bg="white")
    category_name_lable.grid(row=1,column=0,padx=(20),sticky="w")
    category_name_entry=Entry(details_frame,font=("times new roman",15,"bold"),bg="lightyellow")
    category_name_entry.grid(row=1,column=1,pady=20)

    description_lable=Label(details_frame,text="Description",font=("times new roman",15,"bold"),bg="white")
    description_lable.grid(row=2,column=0,padx=(20),sticky="nw")
    description_text=Text(details_frame,width=40,heigh=12,bd=4,bg="lightyellow")
    description_text.grid(row=2,column=1,pady=25)

    button_frame=Frame(category_frame)
    button_frame.place(x=820,y=420)
    
    add_button=Button(button_frame ,text="Add",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:add_category(id_entry.get(),category_name_entry.get(),description_text.get(1.0,END).strip(),treeview))
    add_button.grid(row=0,column=0,padx=20)

    delete_button=Button(button_frame ,text="Delete",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:delete_category(treeview))
    delete_button.grid(row=0,column=1,padx=20)

    clear_button=Button(button_frame ,text="Clear",font=("Times New Roman",15,"bold"),width=10,cursor="hand2",fg="white",bg="blue",command=lambda:clear(id_entry,category_name_entry,description_text,treeview))
    clear_button.grid(row=0,column=2,padx=20)

    treeview_frame=Frame(category_frame,bg="yellow")
    treeview_frame.place(x=780,y=480,height=200,width=540)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))


    treeview = ttk.Treeview(treeview_frame,columns=("id", "name","description"),show="headings",yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)

    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.pack(side=BOTTOM, fill=X)
    scrollx.config(command=treeview.xview)
    scrolly.config(command=treeview.yview)
    treeview.pack(fill=BOTH, expand=1)

    treeview.heading("id", text="Id")
    treeview.heading("name", text="Category Name")
    treeview.heading("description", text="Description")

    treeview.column("id",width=90)
    treeview.column("name",width=200)
    treeview.column("description",width=300)
    treeview_data(treeview)

    treeview_data(treeview)
    treeview.bind("<ButtonRelease-1>",lambda event:select_data(event,id_entry,category_name_entry,description_text,treeview))
    return category_frame