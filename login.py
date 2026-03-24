from tkinter import *
from tkinter import messagebox, simpledialog
import pymysql
import subprocess
import re
from PIL import Image, ImageTk

class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login | StockWise")
        self.root.geometry("1535x812+0+0")
        self.root.resizable(False, False)

        # ===== Variables =====
        self.employee_id = StringVar()
        self.password = StringVar()

        # ===== Initialize DB =====
        self.init_database()

        # ===== GUI Design =====
        self.create_login_form()

    def init_database(self):
        try:
            self.connection = pymysql.connect(host="localhost", user="root", password="1234")
            cursor = self.connection.cursor()

            cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
            self.connection.select_db("inventory_system")

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS login_data (
                    eid VARCHAR(20) PRIMARY KEY,
                    pass VARCHAR(50) NOT NULL,
                    utype VARCHAR(10) NOT NULL
                )
            """)
            self.connection.commit()

            # Create default admin if not exists
            cursor.execute("SELECT * FROM login_data WHERE eid='admin'")
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO login_data (eid, pass, utype) VALUES ('admin', 'admin123', 'Admin')")
                self.connection.commit()

        except Exception as ex:
            messagebox.showerror("Database Error", f"Error initializing database:\n{str(ex)}", parent=self.root)

    def create_login_form(self):
        self.clear_window()

        self.bg_image = Image.open("bck.jpg")
        self.bg_image = self.bg_image.resize((1535, 812), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add heading label at the top
        Label(self.root, text="StockWise", font=("Helvetica", 50, "bold"), fg="white", bg="#001f3f").place(x=0, y=0, relwidth=1)

        frame = Frame(self.root, bg="#415a77", bd=2, relief=RIDGE)
        frame.place(x=550, y=200, width=430, height=400)

        title = Label(frame, text="Login", font=("Time New Roman", 30, "bold"), fg="blue")
        title.pack(pady=20)

        lbl_user = Label(frame, text="Employee ID", font=("Arial", 12), bg="white", anchor="w")
        lbl_user.pack(fill="x", padx=20, pady=(5, 0))
        txt_user = Entry(frame, textvariable=self.employee_id, font=("Arial", 12))
        txt_user.pack(fill="x", padx=20, pady=5)

        lbl_pass = Label(frame, text="Password", font=("Arial", 12), bg="white", anchor="w")
        lbl_pass.pack(fill="x", padx=20, pady=(10, 0))
        txt_pass = Entry(frame, textvariable=self.password, font=("Arial", 12), show="*")
        txt_pass.pack(fill="x", padx=20, pady=5)

        btn_login = Button(frame, text="Login", font=("Arial", 12, "bold"), cursor="hand2",command=self.login)
        btn_login.pack(pady=10)

        btn_forgot = Button(frame, text="Forgot Password?", font=("Arial", 12, "underline","bold"), fg="blue", bd=0, cursor="hand2", command=self.forgot_password)
        btn_forgot.pack(pady=10)

        btn_register = Button(frame, text="Create New Account", font=("Arial", 12, "bold"),cursor="hand2", command=self.create_register_form)
        btn_register.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        eid = self.employee_id.get().strip()
        pwd = self.password.get().strip()

        if eid == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT utype FROM login_data WHERE eid=%s AND pass=%s", (eid, pwd))
            admin = cursor.fetchone()

            if admin:
                utype = admin[0]
                messagebox.showinfo("Success", f"Welcome {eid} ({utype})", parent=self.root)
                self.root.destroy()
                subprocess.Popen(["python", "dashboard.py"])
                return

            cursor.execute("SELECT user_type FROM employee_data WHERE empid=%s AND password=%s", (eid, pwd))
            emp = cursor.fetchone()

            if emp:
                utype = emp[0]
                messagebox.showinfo("Success", f"Welcome {eid} ({utype})", parent=self.root)
                self.root.destroy()
                subprocess.Popen(["python", "user.py"])
                return

            messagebox.showerror("Error", "Invalid ID or Password", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Login failed:\n{str(ex)}", parent=self.root)

    def forgot_password(self):
        eid = self.employee_id.get().strip()
        if eid == "":
            messagebox.showwarning("Input Required", "Please enter your Employee ID to reset password.", parent=self.root)
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM login_data WHERE eid=%s", (eid,))
            user = cursor.fetchone()

            if not user:
                messagebox.showerror("Error", "Employee ID not found", parent=self.root)
                return

            new_password = simpledialog.askstring("Reset Password", f"Enter new password for {eid}:", show='*', parent=self.root)
            if new_password is None or new_password.strip() == "":
                return

            if len(new_password) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters long", parent=self.root)
                return

            if not any(char.isupper() for char in new_password):
                messagebox.showerror("Error", "Password must contain at least one uppercase letter", parent=self.root)
                return

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_password):
                messagebox.showerror("Error", "Password must contain at least one special character", parent=self.root)
                return

            cursor.execute("UPDATE login_data SET pass=%s WHERE eid=%s", (new_password, eid))
            self.connection.commit()
            messagebox.showinfo("Success", "Password has been reset successfully", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Password reset failed:\n{str(ex)}", parent=self.root)

    def create_register_form(self):
        self.clear_window()

        self.bg_image = Image.open("reg.jpg")
        self.bg_image = self.bg_image.resize((1535, 812), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(self.root, text="Create Account", font=("Time New Roman", 20, "bold")).place(x=950, y=200)
        Label(self.root, text="Employee ID", font=("Time New Roman", 14)).place(x=950, y=250)
        Entry(self.root, textvariable=self.employee_id, font=("Time New Roman", 14)).place(x=950, y=285)
        Label(self.root, text="Password", font=("Time New Roman", 14)).place(x=950, y=330)
        Entry(self.root, textvariable=self.password, font=("Time New Roman", 14), show="*").place(x=950, y=365)

        self.user_type = "Admin"

        Button(self.root, text="Register", font=("Time New Roman", 15, "bold"), command=self.register).place(x=950, y=410)
        Button(self.root, text="Back to Login", font=("Time New Roman", 15, "bold"), command=self.create_login_form).place(x=950, y=460)

    def register(self):
        eid = self.employee_id.get().strip()
        pwd = self.password.get().strip()
        utype = "Admin"

        if eid == "" or pwd == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if len(pwd) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long", parent=self.root)
            return

        if not any(char.isupper() for char in pwd):
            messagebox.showerror("Error", "Password must contain at least 1 capital letter", parent=self.root)
            return

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', pwd):
            messagebox.showerror("Error", "Password must contain at least 1 special character", parent=self.root)
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM login_data WHERE eid=%s", (eid,))
            if cursor.fetchone() is not None:
                messagebox.showerror("Error", "Employee ID already exists", parent=self.root)
                return

            cursor.execute("INSERT INTO login_data (eid, pass, utype) VALUES (%s, %s, %s)", (eid, pwd, utype))
            self.connection.commit()
            messagebox.showinfo("Success", "Account created successfully", parent=self.root)
            self.create_login_form()
        except Exception as ex:
            messagebox.showerror("Error", f"Registration failed:\n{str(ex)}", parent=self.root)

# ===== Run the App =====
if __name__ == "__main__":
    root = Tk()
    obj = LoginSystem(root)
    root.mainloop()
