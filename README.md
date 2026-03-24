# 📦 Inventory Management System (IMS)

## 📖 Overview

The Inventory Management System (IMS) is built using **Python and Tkinter** with **MySQL database integration**.
It allows management of employees, products, categories, and suppliers, along with billing functionality.

## 🚀 Features

* 🔐 **User Authentication:** Login system for Admin and Employees

* 🛡️ **Role-Based Access:**

  * **Admin:** Full control (employees, products, categories, suppliers, reports)
  * **Employee:** Access to billing system

* 📊 **CRUD Operations:**

  * Manage Employees
  * Manage Products
  * Manage Categories
  * Manage Suppliers
  * View Bills / Sales

* 🔍 **Search Functionality:**

  * Search Employees
  * Search Suppliers
  * Search Categories
  * Search Products


## ⚙️ Usage

### 🔰 First Time Setup

* If database is empty, create admin user
* Login using Employee ID and Password

## 🔐 Login System

![Login](screenshots/login.png)

Handles user login with:

* Employee ID
* Password

After login:

* Admin → Dashboard
* Employee → Billing

## 📊 Dashboard (Admin Only)

![Dashboard](screenshots/dashboard.png)

Provides access to:

* Employees
* Suppliers
* Products
* Categories
* Sales Overview

## 👨‍💼 Manage Employees

![Employee](screenshots/employee.png)

* Add / Update / Delete Employees
* Search Employees
* Manage employee details

## 📦 Manage Products

![Product](screenshots/product.png)

* Add / Update / Delete Products
* Track stock
* Search products

## 📂 Manage Categories

![Category](screenshots/product.png)

* Add / Delete categories
* View category list

## 🏢 Manage Suppliers

![Supplier](screenshots/supplier.png)

* Add / Update / Delete suppliers
* Maintain supplier records

## 🧾 Billing System (Employee)

![Billing](screenshots/bill.png)

* Generate customer bills
* Add products to cart
* Auto calculation
* QR code generation

## 📌 Future Enhancements

* Export reports (PDF/Excel)
* Web-based version (Flask/Django)
* Barcode scanning
* Analytics dashboard

## 👨‍💻 Author

Prabal Jain

🔗 GitHub: https://github.com/Prabal24

## ⭐ Support

If you like this project, please give it a ⭐ on GitHub!
