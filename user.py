import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import qrcode
from PIL import Image, ImageTk
import time
import subprocess


# Database Connection
def connect_database():
    try:
        connection = pymysql.connect(host="localhost", user="root", password="1234")
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_system")
        cursor.execute("USE inventory_system")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_data(
                id int AUTO_INCREMENT PRIMARY KEY,
                category VARCHAR(100),
                supplier VARCHAR(200),
                name VARCHAR(100),
                price DECIMAL(10,2),
                quantity INT,
                status VARCHAR(50)
            )
        """)
        return cursor, connection
    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return None, None


# Main App
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StockWise")
        self.root.geometry("1200x700")

        self.subtitle_label = tk.Label(self.root, text="Welcome", font=("times new roman", 15), bg="#4d636d", fg="white")
        self.subtitle_label.place(x=0, y=100, relwidth=1) 

        # ======= Header Frame (Logo + Title) =======
        header_frame = tk.Frame(self.root, bg="#010c48", height=80)
        header_frame.pack(fill=tk.X)

        # Load and place logo
        self.logo_img = Image.open("s.jpg")
        self.logo_img = self.logo_img.resize((140, 140), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)
        logo_label = tk.Label(header_frame, image=self.logo_img, bg="#010c48")
        logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Title next to logo
        title_label = tk.Label(header_frame, text="StockWise", font=("Helvetica", 50, "bold"), fg="white", bg="#010c48")
        title_label.pack(side=tk.LEFT, padx=5)

        # ======= Logout Button =======
        logout_btn = tk.Button(header_frame, text="Logout", font=("Times new roman",30,"bold"),
                               bg="White", fg="Red",height="1",width="8", command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=20, pady=20)

        self.update_clock()

        # Customer Details Frame
        customer_frame = tk.LabelFrame(root, text="Customer Details", font=("Time new Roman", 20, "bold"))
        customer_frame.place(x=10, y=150, width=2170, height=100)

        tk.Label(customer_frame, text="Name:", font=("Time new Roman", 15)).grid(row=0, column=0, padx=10, pady=5)
        self.customer_name = tk.Entry(customer_frame, font=("Time new Roman", 15),bg="lightyellow")
        self.customer_name.grid(row=0, column=1, padx=10)

        tk.Label(customer_frame, text="Contact No:", font=("Time new Roman", 15)).grid(row=0, column=2, padx=15)
        self.customer_contact = tk.Entry(customer_frame, font=("Time new Roman", 15),bg="lightyellow")
        self.customer_contact.grid(row=0, column=3, padx=10)

        # Product Frame
        product_frame = tk.LabelFrame(root, text="All Products", font=("Time new Roman", 15, "bold"))
        product_frame.place(x=10, y=270, width=480, height=500)

        tk.Label(product_frame, text="Search By:",font=("Time new Roman", 12,"bold")).pack(pady=2)
        self.search_by = ttk.Combobox(product_frame, values=["Name", "Category", "Supplier"], font=("Time new Roman", 12),state="readonly")
        self.search_by.set("Select")
        self.search_by.pack(pady=2)

        tk.Label(product_frame, text="Search:",font=("Time new Roman", 12,"bold")).pack(pady=2)
        self.search_var = tk.StringVar()
        tk.Entry(product_frame, textvariable=self.search_var).pack(pady=5)
        tk.Button(product_frame, text="Search",font=("Time new Roman", 12,"bold"),bg="blue" , fg="white", command=self.search_product).pack(pady=5)
        tk.Button(product_frame, text="Show All", font=("Time new Roman", 12,"bold"),bg="blue" , fg="white",command=self.fetch_products,).pack(pady=5)

        # Treeview frame
        tree_frame = tk.Frame(product_frame)
        tree_frame.pack(fill=tk.BOTH, expand=1)

        scrollbar_y = tk.Scrollbar(tree_frame, orient="vertical")
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        scrollbar_x = tk.Scrollbar(tree_frame, orient="horizontal")
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.product_list = ttk.Treeview(tree_frame, columns=("id", "category", "supplier", "name", "price", "quantity", "status"),
                                        show='headings', yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        scrollbar_y.config(command=self.product_list.yview)
        scrollbar_x.config(command=self.product_list.xview)

        for col in self.product_list["columns"]:
            self.product_list.heading(col, text=col.capitalize())

        self.product_list.pack(fill=tk.BOTH, expand=1)
        self.product_list.bind("<ButtonRelease-1>", self.select_product)

        # Cart Frame
        cart_frame = tk.LabelFrame(root, text="Cart", font=("Time new Roman", 15, "bold"))
        cart_frame.place(x=505, y=272, width=480, height=500)

        tk.Label(cart_frame, text="Product Name:",font=("Time new Roman", 12, "bold")).pack(pady=5)
        self.prod_name = tk.Entry(cart_frame,font=("Time new Roman", 12),bg="lightyellow")
        self.prod_name.pack(pady=5)

        tk.Label(cart_frame, text="Price:",font=("Time new Roman", 12, "bold")).pack(pady=5)
        self.prod_price = tk.Entry(cart_frame,font=("Time new Roman", 12),bg="lightyellow")
        self.prod_price.pack(pady=5)

        tk.Label(cart_frame, text="Quantity:",font=("Time new Roman", 12, "bold")).pack(pady=5)
        self.prod_qty = tk.Entry(cart_frame,font=("Time new Roman", 12),bg="lightyellow")
        self.prod_qty.pack(pady=5)

        tk.Button(cart_frame, text="Add",font=("Time new Roman", 12,"bold"),bg="blue" , fg="white", command=self.add_to_cart).pack(pady=10)
        tk.Button(cart_frame, text="Update Cart",font=("Time new Roman", 12,"bold"),bg="blue" , fg="white", command=self.add_to_cart).pack(pady=10)

        self.cart_tree = ttk.Treeview(cart_frame, columns=("name", "price", "qty"), show='headings', height=10)
        for col in ("name", "price", "qty"):
            self.cart_tree.heading(col, text=col.capitalize())
        self.cart_tree.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        self.cart = []

        # Billing Area
        bill_frame = tk.LabelFrame(root, text="Billing Area", font=("Time new Roman", 15, "bold"))
        bill_frame.place(x=1000, y=251, width=480, height=520)

        self.bill_area = tk.Text(bill_frame, font=("Arial", 12),bg="lightyellow")
        self.bill_area.pack(expand=1, fill=tk.BOTH)

        btn_frame = tk.Frame(bill_frame)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Generate Bill", font=("Time new Roman", 15, "bold"),
          bg="blue", fg="white", command=self.generate_bill).pack(side=tk.LEFT, padx=10)

        tk.Button(btn_frame, text="Clear All", font=("Time new Roman", 15, "bold"),
          bg="blue", fg="white", command=self.clear_all).pack(side=tk.LEFT, padx=10)

        self.fetch_products()

    def update_clock(self):
        date_time = time.strftime("%I:%M:%S %p on %A, %B %d, %Y")
        self.subtitle_label.config(text=f"Welcome\t\t\t\t\t\t\t{date_time}")
        self.subtitle_label.after(1000, self.update_clock)

    def fetch_products(self):
        cursor, connection = connect_database()
        if cursor:
            cursor.execute("USE inventory_system")
            cursor.execute("SELECT id, category, supplier, name, price, quantity, status FROM product_data WHERE status='Active'")
            rows = cursor.fetchall()
            self.product_list.delete(*self.product_list.get_children())
            for row in rows:
                self.product_list.insert('', tk.END, values=row)
            connection.close()

    def search_product(self):
        if self.search_by.get() == "":
            messagebox.showinfo("Warning", "Please select a search filter.")
            return
        if self.search_var.get() == "":
            messagebox.showwarning("Warning", "Please enter a search value.")
            return

        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute("USE inventory_system")

        query = f"SELECT * FROM product_data WHERE {self.search_by.get()} = %s AND status='Active'"
        cursor.execute(query, (self.search_var.get(),))

        records = cursor.fetchall()
        self.product_list.delete(*self.product_list.get_children())
        if not records:
            messagebox.showinfo("No Results", "No matching products found.")
        else:
            for record in records:
                self.product_list.insert('', tk.END, values=record)
        connection.close()

    def select_product(self, event):
        selected = self.product_list.focus()
        values = self.product_list.item(selected, 'values')
        if values:
            self.prod_name.delete(0, tk.END)
            self.prod_price.delete(0, tk.END)
            self.prod_qty.delete(0, tk.END)
            self.prod_name.insert(0, values[3])
            self.prod_qty.insert(0, values[5])
            self.prod_price.insert(0, values[4])

    def add_to_cart(self):
        try:
            name = self.prod_name.get()
            price = float(self.prod_price.get())
            qty = int(self.prod_qty.get())
            if name == "" or price <= 0 or qty <= 0:
                raise ValueError
            updated = False
            for i, item in enumerate(self.cart):
                if item[0] == name:
                    self.cart[i] = (name, price, qty)
                    updated = True
                    break
            if not updated:
                self.cart.append((name, price, qty))
            self.update_cart_display()
            messagebox.showinfo("Cart", f"{name} added/updated in cart.")
        except:
            messagebox.showerror("Input Error", "Enter valid product name, price and quantity.")

    def update_cart_display(self):
        self.cart_tree.delete(*self.cart_tree.get_children())
        for item in self.cart:
            self.cart_tree.insert('', tk.END, values=item)

    def generate_bill(self):
        if not self.cart:
            messagebox.showwarning("No Items", "Cart is empty.")
            return
        self.bill_area.delete('1.0', tk.END)
        self.bill_area.insert(tk.END, f"Customer: {self.customer_name.get()}\nContact: {self.customer_contact.get()}\n")
        self.bill_area.insert(tk.END, f"\n{'Item':20}{'Qty':>5}{'Price':>10}\n")
        total = 0
        for item in self.cart:
            name, price, qty = item
            line_total = price * qty
            total += line_total
            self.bill_area.insert(tk.END, f"{name:20}{qty:>5}{line_total:>10.2f}\n")
        tax = total * 0.1
        net = total + tax
        self.bill_area.insert(tk.END, f"\nTotal: {total:.2f}\nTax (10%): {tax:.2f}\nNet Pay: {net:.2f}\n")
        self.generate_qr(f"Customer: {self.customer_name.get()} | Net Pay: ₹{net:.2f}")

    def generate_qr(self, data):
        img = qrcode.make(data)
        img.save("bill_qr.png")
        qr_img = Image.open("bill_qr.png")
        qr_img = qr_img.resize((120, 120))
        self.qr = ImageTk.PhotoImage(qr_img)
        if hasattr(self, 'qr_label'):
            self.qr_label.config(image=self.qr)
        else:
            self.qr_label = tk.Label(self.root, image=self.qr)
            self.qr_label.place(x=1040, y=600)

    def clear_all(self):
        self.customer_name.delete(0, tk.END)
        self.customer_contact.delete(0, tk.END)
        self.prod_name.delete(0, tk.END)
        self.prod_price.delete(0, tk.END)
        self.prod_qty.delete(0, tk.END)
        self.cart.clear()
        self.bill_area.delete('1.0', tk.END)
        self.update_cart_display()
        self.fetch_products()
        if hasattr(self, 'qr_label'):
            self.qr_label.destroy()
            del self.qr_label

    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if confirm:
            self.root.destroy()
            subprocess.Popen(["python", "login.py"])


if __name__ == '__main__':
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
