from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import pymysql



def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employee_data(
                empid INT PRIMARY KEY, 
                name VARCHAR(100),
                email VARCHAR(100), 
                gender VARCHAR(50),
                dob VARCHAR(30),
                contact VARCHAR(30),
                employment_type VARCHAR(50),
                education VARCHAR(100),
                work_shift VARCHAR(50),
                address VARCHAR(100),
                doj VARCHAR(30),
                salary VARCHAR(50),
                user_type VARCHAR(50),
                password VARCHAR(50)
            )
        """)
    except Exception as e:
        messagebox.showerror("Error", f"Database connectivity issue:\n{str(e)}\nPlease open MySQL command line.")


    