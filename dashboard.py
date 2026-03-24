from tkinter import*
from PIL import Image, ImageTk
from employees import employee_form
from supplier import supplier_form
from category import category_form
from products import product_form
from tkinter import messagebox
import time
import pymysql
from subprocess import Popen

#TIME
# Database connection function
def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor = connection.cursor()
        return cursor, connection
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None, None

def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute("use inventory_system")
    cursor.execute("SELECT* from employee_data")
    records=cursor.fetchall()
    total_emp_count_label.config(text=len(records))

    cursor.execute("SELECT* from supplier_data")
    records=cursor.fetchall()
    total_sup_count_label.config(text=len(records))

    cursor.execute("SELECT* from category_data")
    records=cursor.fetchall()
    total_cat_count_label.config(text=len(records))

    cursor.execute("SELECT* from product_data")
    records=cursor.fetchall()
    total_prod_count_label.config(text=len(records))


    date_time=time.strftime("%I:%M:%S %p on %A,%B %d,%Y ")
    subtitleLable.config(text=f"Welcome\t\t\t\t\t\t\t{date_time}")
    subtitleLable.after(1000,update)



current_frame=None
def show_from(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)

#Gui Part  
window=Tk()

#window = Tk()
window.title('Dashboard')
window.state("zoomed")
window.attributes("-fullscreen", True)
window.resizable(0, 0)
window.config(bg='White')

# Load and display the background image
dashboard_bg_img = Image.open("grocery bg.png")  # Replace with your image file
dashboard_bg_img = dashboard_bg_img.resize((window.winfo_screenwidth(), window.winfo_screenheight()), Image.Resampling.LANCZOS)
dashboard_bg_image = ImageTk.PhotoImage(dashboard_bg_img)

bg_label = Label(window, image=dashboard_bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# Escape se exit karne ka function
def exit_fullscreen(event=None):
    window.attributes("-fullscreen", False)

# Escape key bind
window.bind("<Escape>", exit_fullscreen)

# Exit fullscreen button
fullscreen_exit_button = Button(window, text="Exit Fullscreen", command=exit_fullscreen,bg="black", fg="white", font=("Times New Roman", 30,"bold"))
fullscreen_exit_button.place(x=1050, y=10 )


#from PIL import Image, ImageTk

# Load and resize the image for the title bar
header_img = Image.open("s.jpg")  # Replace with correct path
header_img = header_img.resize((100, 200), Image.Resampling.LANCZOS)  # Pillow 10+ fix
bg_image = ImageTk.PhotoImage(header_img)

# Create label with image + text
titleLabel = Label(window, image=bg_image, compound=LEFT, text="  StockWise", font=("Helvetica", 50, "bold"), bg="#010c48", fg="white", anchor='w', padx=30)
titleLabel.place(x=0, y=0, relwidth=1, height=100)


def logout():
    window.destroy()  # Closes the dashboard
    Popen(["python", "login.py"])
    window.destroy()

logoutbutton=Button(window,text = "Logout",font=("Times new roman",30,"bold"),fg="red",command=logout)
logoutbutton.place(x=1370,y=10)

#Clock
subtitleLable = Label(window,text="Welcome \t\t Date: 07-05-2025 \t\t Time: 06:30:32:",font=("times new roman",15),bg="#4d636d",fg="white")
subtitleLable.place(x=0,y=100,relwidth=1)

leftFrame=Frame(window,bg="lightpink")
#leftFrame.place(x=0,y=128,width=350,height=565)
leftFrame.place(x=0, y=128, width=250, relheight=1)


logoImage = PhotoImage(file="checklist.png")
imageLabel=Label(leftFrame,image=logoImage)
imageLabel.pack()

#Menu
menulable=Label(leftFrame,text="Menu",font=("Times new Roman",20),bg="#009688")
menulable.pack(fill=X)

#Button
employee_icon=PhotoImage(file="employee.png")
employee_Button=Button(leftFrame,image=employee_icon,compound=LEFT,text="Employee",font=("Times new Roman",20,"bold"),anchor="w",padx=10,command=lambda :show_from(employee_form))#(window))
employee_Button.pack(fill=X)

supplier_icon=PhotoImage(file="supplier.png")
supplier_Button=Button(leftFrame,image=supplier_icon,compound=LEFT,text="Supplier",font=("Times new Roman",20,"bold"),anchor="w",padx=10,command=lambda:show_from(supplier_form))#(window))
supplier_Button.pack(fill=X)

Categories_icon=PhotoImage(file="categories.png")
Categories_Button=Button(leftFrame,image=Categories_icon,compound=LEFT,text="Categories",font=("Times new Roman",20,"bold"),anchor="w",padx=10,command=lambda:show_from(category_form))#(window))
Categories_Button.pack(fill=X)

product_icon=PhotoImage(file="product.png")
product_Button=Button(leftFrame,image=product_icon,compound=LEFT,text="Products",font=("Times new Roman",20,"bold"),anchor="w",padx=10,command=lambda:show_from(product_form))#(window))
product_Button.pack(fill=X)

"""Sale_icon=PhotoImage(file="Sale.png")
Sale_Button=Button(leftFrame,image=Sale_icon,compound=LEFT,text="Sale",font=("Times new Roman",20,"bold"),anchor="w",padx=10)
Sale_Button.pack(fill=X)"""

# Add a spacer frame to fill the remaining vertical space
spacer = Frame(leftFrame, bg="white")
spacer.pack(expand=True, fill=BOTH)


"""Exit_icon=PhotoImage(file="log-out.png")
Exit_Button=Button(leftFrame,image=Exit_icon,compound=LEFT,text="Exit",font=("Times new Roman",20,"bold"),anchor="w",padx=10)
Exit_Button.pack(fill=X)"""
#4 frame
emp_frame=Frame(window,bg="#2C3E50",bd=3,relief=RIDGE)
emp_frame.place(x=400,y=158,height=190,width=300)
total_emp_icon=PhotoImage(file="staff.png")
total_emp_icon_label=Label(emp_frame,image=total_emp_icon)
total_emp_icon_label.pack()

total_emp_label = Label(emp_frame,text="Total Employee",bg="#2C3E50",fg="white",font=("times new roman ", 15,"bold"))
total_emp_label.pack()

#total_emp_label = Label(emp_frame,text= 0,bg="#2C3E50",fg="white",font=("times new roman ", 30,"bold"))
#total_emp_label.pack()

total_emp_count_label =Label(emp_frame,text="0",bg="#2C3E50",fg="white",font=("times new roman", 30,"bold"))
total_emp_count_label.pack()

#Suppliers
sup_frame=Frame(window,bg="#8E44AD",bd=3,relief=RIDGE)
sup_frame.place(x=800,y=158,height=190,width=300)
total_sup_icon=PhotoImage(file="sup.png")
total_sup_icon_label=Label(sup_frame,image=total_sup_icon)
total_sup_icon_label.pack()

total_sup_label = Label(sup_frame,text="Total Suppliers",bg="#8E44AD",fg="white",font=("times new roman ", 15,"bold"))
total_sup_label.pack()

total_sup_count_label = Label(sup_frame,text= 0,bg="#8E44AD",fg="white",font=("times new roman ", 30,"bold"))
total_sup_count_label.pack()

#Categorie 

cat_frame=Frame(window,bg="blue",bd=3,relief=RIDGE)
cat_frame.place(x=400,y=358,height=190,width=300)
total_cat_icon=PhotoImage(file="cat.png")
total_cat_icon_label=Label(cat_frame,image=total_cat_icon)
total_cat_icon_label.pack()

total_cat_label = Label(cat_frame,text="Total Categories",bg="blue",fg="white",font=("times new roman ", 15,"bold"))
total_cat_label.pack()

total_cat_count_label = Label(cat_frame,text= 0,bg="blue",fg="white",font=("times new roman ", 30,"bold"))
total_cat_count_label.pack()

#Product

prod_frame=Frame(window,bg="pink",bd=3,relief=RIDGE)
prod_frame.place(x=800,y=358,height=190,width=300)
total_prod_icon=PhotoImage(file="prod.png")
total_prod_icon_label=Label(prod_frame,image=total_prod_icon)
total_prod_icon_label.pack()

total_prod_label = Label(prod_frame,text="Total Products",bg="pink",fg="white",font=("times new roman ", 15,"bold"))
total_prod_label.pack()

total_prod_count_label = Label(prod_frame,text= 0,bg="pink",fg="white",font=("times new roman ", 30,"bold"))
total_prod_count_label.pack()

#sales

"""sales_frame=Frame(window,bg="silver",bd=3,relief=RIDGE)
sales_frame.place(x=600,y=538,height=170,width=280)
total_sales_icon=PhotoImage(file="sale.png")
total_sales_icon_label=Label(sales_frame,image=total_sales_icon)
total_sales_icon_label.pack()

total_sales_label = Label(sales_frame,text="Total Sales",bg="silver",fg="white",font=("times new roman ", 15,"bold"))
total_sales_label.pack()

total_sales_label = Label(sales_frame,text= 0,bg="silver",fg="white",font=("times new roman ", 30,"bold"))
total_sales_label.pack()"""
update()


window.mainloop()
