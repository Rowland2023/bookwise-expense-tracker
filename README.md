# 📘 BookWise Expense Tracker

A Django-based web application designed to track and visualize expenses related to book production, distribution, and other categories. It features data import from spreadsheets, a robust backend API, and an interactive expense report view using Chart.js.

## 📸 Screenshots

### Admin Dashboard
![Admin Interface](statics/screenshot/admin_dashboard.png)

### Expense Chart View
![Expense Chart](statics/screenshot/expense_chart.png)

## ✨ Features

* **Data Management:**
    * Manage `Book`, `Author`, `Publisher`, `Category`, and `Expense` records.
    * Robust data models with relationships (Foreign Keys, Many-to-Many).
* **CSV Data Import:**
    * Custom Django management command to efficiently import book and expense data from CSV spreadsheets into the database.
    * Includes data cleaning, type conversion, and idempotent `update_or_create` logic to prevent duplicates on re-runs.
* **Expense Reporting & Visualization:**
    * Interactive web-based report view to visualize monthly expenses.
    * Utilizes **Chart.js** for dynamic bar chart rendering of expense breakdowns by month.
    * Allows users to download the generated chart as a PNG image or export it as a PDF document (using jsPDF).
* **Admin Interface:**
    * Django's built-in admin interface for easy management and inspection of all data models.
* **Scalable Backend:**
    * Built with Django, providing a solid foundation for future feature expansion and API development.

## 🚀 Technologies Used

* **Backend:** Python, Django
* **Database:** SQLite (default, easily configurable for PostgreSQL/MySQL)
* **Data Import:** Python `csv` module, Django Management Commands
* **Data Visualization:** Chart.js
* **PDF Export:** jsPDF
* **Styling:** Basic CSS
* **Version Control:** Git

## ⚙️ Setup & Installation

Follow these steps to get the project up and running on your local machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Rowland2023/bookwise-expense-tracker.git](https://github.com/Rowland2023/bookwise-expense-tracker.git)
cd bookwise-expense-tracker/myproject # Navigate into your Django project root

