# M Faqih Asshiddik - CRUD for Data Reimbursements

from tabulate import tabulate
from datetime import datetime

user = {"username": "admin", "password": "purwadhika37"}

data_employeeID = {
    "25001": "Tania",
    "25002": "Bagus",
    "25003": "Fauzan",
    "25004": "Yoga",
    "25005": "Ullil",
}

data_reimbursements = [
    {
        "expense_id": "00001",
        "employee_id": "25001",
        "name": "Tania",
        "category": "Meals",
        "amount": 300000,
        "date": "2024-10-5",
        "status": "Rejected",
        "description": "The expense is rejected"
    },
    {
        "expense_id": "00002",
        "employee_id": "25002",
        "name": "Bagus",
        "category": "Insurance",
        "amount": 500000,
        "date": "2024-10-13",
        "status": "Under Review",
        "description": "The expense is currently under review"
    },
    {
        "expense_id": "00003",
        "employee_id": "25003",
        "name": "Fauzan",
        "category": "Transport",
        "amount": 200000,
        "date": "2024-10-18",
        "status": "Approved",
        "description": "The expense is approved"
    },
    {
        "expense_id": "00004",
        "employee_id": "25004",
        "name": "Yoga",
        "category": "Certification",
        "amount": 5000000,
        "date": "2024-10-20",
        "status": "Under Review",
        "description": "The expense is currently under review"
    },
    {
        "expense_id": "00005",
        "employee_id": "25005",
        "name": "Ullil",
        "category": "Parking",
        "amount": 350000,
        "date": "2024-10-30",
        "status": "Approved",
        "description": "The expense is approved"
    }
]

def new_expense_id():
    if not data_reimbursements:
        return "00001"                                   # kalau misal tidak ada data, maka jadi start di 00001
    last_id = int(data_reimbursements[-1]["expense_id"]) # -1 untuk mengambil di list terakhir untuk ditambahkan menjadi expense_id
    return f"{last_id + 1:05}"                           # menggunakan 05 karena ingin menjadi 5 angka # +1 sebagai increment ke baris bawah

def login():
    while True:
        username = input("Username: ")
        password = input("Password: ")
        if username == user["username"] and password == user["password"]:
            print("Login Successful!")
            return True
        else:
            print("Invalid login.")
            try_again = input("Try again? (Y/N): ")
            if try_again == 'N':
                print("Exiting.")
                return False

def display_menu():
    print("\nBusiness Reimbursement System")
    print("1. Add Reimbursement")
    print("2. View Reimbursements")
    print("3. Update Reimbursement")
    print("4. Delete Reimbursement")
    print("5. Exit")

def validate_date(date_string):
    parts = date_string.split("-")

    if len(parts) != 3:
        print("Invalid date format. Use yyyy-mm-dd.")
        return None
    
    day, month, year = parts

    if not(day.isdigit() and month.isdigit() and year.isdigit()):
        print("Date must contain only numbers.")
        return None
    
    day = int(day)
    month = int(month)
    year = int(year)

    if year < 1987 or year > 2050:
        print("Invalid year. Year must be between 1987 and 2050.")
        return None
    
    days_in_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month < 1 or month > 12:
        print("Invalid month. Month must be between 1 and 12.")
        return None
    
    if day < 1 or day > days_in_month[month]:
        print(f"Invalid day for month {month}. Day must be between 1 and {days_in_month[month]}.")
        return None
    
    if month == 2 and day == 29:
        if not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            print("Invalid date. Not a leap year.")
            return None
        
    return datetime(day, month, year)

def add_reimbursement():
    print("\nAdd New Reimbursement")
    expense_id = new_expense_id()
    employee_id = input("Employee ID: ")
    name = data_employeeID.get(employee_id, "Unknown")
    if name == "Unknown":
        print("Employee not found in the database.")
        return
    
    while True:
        amount = input("Amount: ")
        if amount.isdigit():
            amount = int(amount)
            break
        else:
            print("Invalid input.")

    category = input("Category: ")
    date = input("Date (yyyy-mm-dd): ")
    status = input("Status: ")  
    description = input("Description: ")

    data_reimbursements.append({
        "expense_id": expense_id,
        "employee_id": employee_id,
        "name": name,
        "amount": amount,
        "category": category,
        "date": validate_date(date),
        "status": status,
        "description": description
    })

    data_reimbursements.sort(key=lambda x: x["expense_id"])        
    print(f"Reimbursement added successfully with Expense ID: {expense_id}")

def view_reimbursements():
    print("\nAll Reimbursements")
    if not data_reimbursements:
        print("No datas found.")
        return

    headers = ["Expense ID", "Employee ID", "Name", "Category", "Amount", "Date", "Status", "Description"]
    table = [[
        item["expense_id"],
        item["employee_id"],
        item["name"],
        item["category"],
        f"Rp{item['amount']:,}",
        item.get("date", "N/A"),
        item["status"],
        item["description"]
    ] for item in data_reimbursements]

    print(tabulate(table, headers, tablefmt="grid"))

def update_reimbursement():
    print("\nUpdate Reimbursement")
    expense_id = input("Enter Expense ID to update: ")
    for item in data_reimbursements:
        if item["expense_id"] == expense_id:
            print("\nCurrent Item:")
            print(item)

            valid_statuses = ["Under Review", "Approved", "Rejected"]
            while True:
                new_status = input("New Status (Under Review/Approved/Rejected): ")
                if new_status in valid_statuses:
                    item["status"] = new_status
                    break
                else: 
                    print(f"Invalid status. Please choose from {valid_statuses}.")
            item["description"] = input("New Description: ")
            print("Reimbursement updated successfully!")
            return
    print("Item not found.")

def delete_reimbursement():
    print("\nDelete Reimbursement")
    expense_id = input("Enter Expense ID to delete: ")
    for item in data_reimbursements:
        if item["expense_id"] == expense_id:
            data_reimbursements.remove(item)
            print("Reimbursement deleted successfully!")
            return
    print("Item not found.")

# Main Application
def main():
    if login():
        while True:
            display_menu()
            choice = input("Enter your choice (1-5): ")
            if choice == "1":
                add_reimbursement()
            elif choice == "2":
                view_reimbursements()
            elif choice == "3":
                update_reimbursement()
            elif choice == "4":
                delete_reimbursement()
            elif choice == "5":
                print("Exiting the system.")
                break
            else:
                print("Invalid choice. Please try again.")

main()

