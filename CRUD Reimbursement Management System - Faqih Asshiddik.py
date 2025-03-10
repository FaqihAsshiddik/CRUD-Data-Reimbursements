from tabulate import tabulate
from datetime import datetime

users = {
    "admin": {
        "password": "purwadhika37",
        "role": "admin",
        "name": "Administrator",
        "employee_id": None                     # Admins don't need employee IDs
    },

    "manager": {
        "password": "purwadhika50",
        "role": "manager",
        "name": "Brian",
        "employee_id": None                     
    }
}

data_employeeID = {
    "25001": "Tania",
    "25002": "Bagus",
    "25003": "Fauzan",
    "25004": "Yoga",
    "25005": "Ullil",
}

# Add employee as users
for emp_id, name in data_employeeID.items():
    username = f"emp_{emp_id}"              # Create usernames based on employee IDs
    users[username] = {
        "password": f"pass_{emp_id}",       # Simple default passwords
        "role": "employee",
        "name": name,
        "employee_id": emp_id  
    }

categories = ["Meals", "Transport", "Accommodation", "Office Supplies", "Insurance", 
              "Certification", "Parking", "Client Entertainment", "Conference", "Other"]

reimbursement_cap = {
    "Meals": 500000, 
    "Transport": 750000, 
    "Accommodation": 2000000, 
    "Office Supplies": 1000000, 
    "Insurance": 5000000, 
    "Certification": 7500000, 
    "Parking": 350000, 
    "Client Entertainment": 1500000, 
    "Conference": 500000, 
    "Other" : 500000
}

data_reimbursements = [
    {
        "expense_id": "00001",
        "employee_id": "25001",
        "name": "Tania",
        "category": "Meals",
        "amount": 300000,
        "date": "2024-10-05",
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

deletion_logs = []

def new_expense_id():
    if not data_reimbursements:
        return "00001"                                   
    last_id = int(data_reimbursements[-1]["expense_id"]) 
    return f"{last_id + 1:05}" 

def validate_date(date_string):
    try: 
        if not all(c.isdigit() or c == '-' for c in date_string):
            raise ValueError("Date should only contain digits and hyphens.")
    
        parts = date_string.split("-")
        if len(parts) != 3:
            raise ValueError("Invalid date format. Use yyyy-mm-dd.")
    
        year, month, day = map(int, parts)

        # Validate ranges of year
        if year < 1987 or year > 2050:
            raise ValueError("Invalid year. Year must be between 1987 and 2050.")
    
        # Validate ranges of month
        days_in_month = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if month < 1 or month > 12:
            raise ValueError("Invalid month. Month must be between 1 and 12.")

        # Validate ranges of day    
        if day < 1 or day > days_in_month[month]:
            raise ValueError(f"Invalid day for month. Day must be between 1 and {days_in_month[month]} for month {month}.")
    
        # Leap year check
        if month == 2 and day == 29:
            if not (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
                raise ValueError(f"Invalid date. {year} is not a leap year.")
                 
        # Ensure date is not in the future
        current_date = datetime.now().date()
        input_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        if input_date > current_date:
            raise ValueError("Date cannot be in the future.")
        
        # Return validated data as string in consitent format
        return f"{year}-{month:02d}-{day:02d}"
    except ValueError as e:
        print(f"Date validation error: {str(e)}")
        return None
    
def validate_category(category):
    if category not in categories:
        print(f"Error: '{category}' is not a valid reimbursement category.")
        print(f"Valid categories are: {', '.join(categories)}")
        return False
    return True

def validate_amount(amount_str, category):
    try:
        if not amount_str.isdigit():
            raise ValueError("Amount must be a number")

        amount = int(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
        
        if category in reimbursement_cap and amount > reimbursement_cap[category]:
            raise ValueError(f"Amount exceeds maximum allowed for {category} (Rp{reimbursement_cap[category]:,})")
        return amount
    
    except ValueError as e:
        print(f"Amount validation error: {str(e)}")
        return None                          

def login():
    current_user = {"username": None, "role": None, "employee_id": None}

    while True:
        username = input("Username: ")
        password = input("Password: ")

        if username in users and password == users[username]["password"]:
            print("Login Successful!")
            current_user["username"] = username
            current_user["role"] = users[username]["role"]
            current_user["employee_id"] = users[username]["employee_id"]
            current_user["name"] = users[username]["name"]

            print(f"Welcome, {current_user['name']}! You are logged in as a {current_user['role']}")
            return current_user

        else:
            print("Invalid login.")
            try_again = input("Try again? (Y/N): ")
            if try_again.upper() == 'N':
                print("Exiting.")
                return None
            
def has_permission(user, action, resource = None):
    """Check if a user has permission to perform an action.
    
    Args:
        user: The current user dictionary
        action: The action to check (view, add, update, delete, approve)
        resource: Optional resource to check (e.g, expense_id)

    Returns: 
        Boolean indicating whether the user has permission
    """
    # If no user is logged in, no permissions
    if not user or not user["username"]:
        return False
    
    role = user["role"]

    # Admin has full control
    if role == "admin":
        return True
    
    # Manager permissions
    if role == "manager":
        if action in ["view", "update", "approve"]:
            return True
        if action == "add":
            return True
        return False                                # Managers can't delete
    
    # Employee permisions
    if role == "employee":
        if action == "add":
            return True
        if action == "view" and resource:
            # Check if viewing own reimbursement
            if resource == "all":
                return True
            # Check if specific reimbursement belongs to the employee
            for item in data_reimbursements:
                if item["expense_id"] == resource and item["employee_id"] == user["employee_id"]:
                    return True     
        return False

    return False
    
def add_reimbursement(user):
    print("\nAdd New Reimbursement")
    expense_id = new_expense_id()
    
    # Employee validation
    if user["role"] == "employee":
        employee_id = user["employee_id"]
        name = user["name"]
    else:
        # Admin and manager can add reimbursements for any employee
        print("\nAvailable employees: ")
        for id, name in data_employeeID.items():
                print(f"  {id}: {name}")

        while True:
            employee_id = input("Employee ID: ")
            if employee_id in data_employeeID:
                name = data_employeeID[employee_id]
                break
            print("Employee not found in the database. Available employee IDs")
    
    # Category selection
    print("\nAvailable categories: ")
    for i, cat in enumerate(categories, 1):
        print(f"  {i}. {cat} (Max: Rp{reimbursement_cap[cat]:,})")

    while True:
        category_input = input("\nCategory (enter name or number): ")
        
        # Selection by number
        if category_input.isdigit() and 1 <= int(category_input) <= len(categories):
            category = categories[int(category_input) - 1]
            break
        
        # Or by name
        elif validate_category(category_input):
            category = category_input
            break
    
    # Amount validation
    while True:
        amount_str = input(f"Amount(max Rp{reimbursement_cap[category]:,}): ")
        amount = validate_amount(amount_str, category)
        if amount is not None:
            break

    # Date validation
    while True:
        date_input = input("Date (yyyy-mm-dd): ")
        validated_date = validate_date(date_input)
        if validated_date is not None:
            break

    # Status validation
    valid_statuses = ["Under Review", "Approved", "Rejected"]
    print("\nStatus options: ")
    for i, status in enumerate(valid_statuses, 1):
        print(f"  {i}. {status}")

    while True:
        status_input = input("\nStatus (enter name or number): ")
        if status_input.isdigit() and 1 <= int(status_input) <= len(valid_statuses):
            status = valid_statuses[int(status_input) - 1]
            break
        elif status_input in valid_statuses:
            status = status_input
            break
        else:
            print(f"Invalid status. Please choose from {valid_statuses}")

    # Description 
    print("\nPlease provide a description for this expense (e.g, purpose, location, participants)")
    description = input("Description: ")
    
    # Confirmation 
    print("\nReimbursement Summary: ")
    print(f"Employee: {name} (ID: {employee_id})")
    print(f"Category: {category}")
    print(f"Amount: Rp{amount:,}")
    print(f"Date: {validated_date}")
    print(f"Status: {status}")
    print(f"Description: {description}")

    confirm = input("\nConfirm addition? (Y/N): ").upper()
    if confirm != 'Y':
        print("Addition cancelled.")
        return

    # Add to data
    data_reimbursements.append({
        "expense_id": expense_id,
        "employee_id": employee_id,
        "name": name,
        "amount": amount,
        "category": category,
        "date": validated_date,
        "status": status,
        "description": description
    })

    data_reimbursements.sort(key=lambda x: x["expense_id"])        
    print(f"Reimbursement added successfully with Expense ID: {expense_id}")

def view_reimbursements(user):
    if user["role"] == "employee":
        print(f"\nReimbursements for {user['name']}")
        # Filter to only show employee's own reimbursements
        filtered_data = [item for item in data_reimbursements if item["employee_id"] == user["employee_id"]]
    else:
        print("\nAll Reimbursements")
        filtered_data = data_reimbursements
    if not filtered_data:
        print("No reimbursements found.")
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
    ] for item in filtered_data]

    print(tabulate(table, headers, tablefmt="grid"))

def approve_reimbursement(user):
    if user["role"] not in ["admin", "manager"]:
        print("You don't have permission to approve reimbursements.")
        return
    
    print("\nPending Reimbursements.")
    pending = [item for item in data_reimbursements if item["status"] == "Under Review"]

    if not pending:
        print("No pending reimbursements to review.")
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
    ] for item in pending]

    print(tabulate(table, headers, tablefmt="grid"))

    while True:
        expense_id = input("\nEnter Expense ID to review (or 'cancel' to go back): ")
        if expense_id.lower() == 'cancel':
            return
        
        # Find the reimbursement
        found_item = None
        for item in pending:
            if item["expense_id"] == expense_id:
                found_item = item
                break

        if found_item:
            break
        print("Item not found or not pending. Please try again.")

    # Show details 
    print("\nReimbursement Details: ")
    for key, value in found_item.items():
        if key == "amount":
            print(f"{key}: Rp{value:,}")
        else:
            print(f"{key}: {value}")

    # Get Decision
    print("\nPlease review this reimbursement: ")
    print("1. Approve")
    print("2. Reject")
    print("3. Keep Under Review")

    decision = input("\nYour decision (1-3): ")

    if decision == "1":
        found_item["status"] = "Approved"
        found_item["description"] = f"The expense is approved by {user['name']} on {datetime.now().strftime('%Y-%m-%d')}"
        print("Reimbursement approved successfully.")
    elif decision == "2":
        reason = input("Reason for rejection: ")
        found_item["status"] = "Rejected"
        found_item["description"] = f"The expense is rejected: {reason} by {user['name']} on {datetime.now().strftime('%Y-%m-%d')}"
        print("Reimbursement rejected successfully.")
    else:
        print("Reimbursement kept under review.")

def update_reimbursement(user):
    print("\nUpdate Reimbursement")

    # For employees, only show their reimbursements
    if user["role"] == "employee":
        filtered_data = [item for item in data_reimbursements if item["employee_id"] == user["employee_id"] and item["status"] == "Under Review"]

        if not filtered_data:
            print("You have no pending reimbursements to update.")
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
        ] for item in filtered_data]

        print("\nYour Pending Reimbursements: ")
        print(tabulate(table, headers, tablefmt="grid"))
    else:
        # Admins and managers can see all
        view_reimbursements(user)

    while True:
        expense_id = input("\nEnter Expense ID to update (or 'cancel' to go back): ")
        if expense_id.lower() == 'cancel':
            return
        
        # Check permission to update this specific reimbursements
        if not has_permission(user, "update", expense_id):
            print("You don't have permission to update this reimbursement.")
            if user["role"] == "employee":
                print("You can only update your own pending reimbursements.")
            return
        
        # Find the reimbursement
        found_item = None
        for item in data_reimbursements:
            if item["expense_id"] == expense_id:
                found_item = item
                break

        if found_item:
            # For employees, double-check it's their own and pending
            if user["role"] == "employee" and (
                found_item["employee_id"] != user["employee_id"] or
                found_item["status"] != "Under Review"
            ):
                print("You can only update your own pending reimbursements.")
                return
            break

        print("Item not found. Please try again.")

    # Show current values
    print("\nCurrent Reimbursement Details: ")
    for key, value in found_item.items():
        if key == "amount":
            print(f"{key}: Rp{value:,}")
        else:
            print(f"{key}: {value}")

    if user["role"] == "admin":
        print("\nWhat would you like to update?")
        print("1. Category")
        print("2. Amount")
        print("3. Date")
        print("4. Status")
        print("5. Description")
        print("6. All fields")
        print("7. Cancel update")
        max_option = 7

    elif user["role"] == "manager":
        print("\nWhat would you like to update?")
        print("1. Status (Approve/Reject)")
        print("2. Description")
        print("3. Cancel Update")
        max_option = 3
    
    else:
        print("\nWhat would you like to update?")
        print("1. Category")
        print("2. Amount")
        print("3. Date")
        print("4. Description")
        print("5. Cancel update")
        max_option = 5  

    choice = input(f"\nEnter your choice (1-{max_option}): ")

    # Validate choice
    if not choice.isdigit() or int(choice) < 1 or int(choice) > max_option:
        print("Invalid choice.")
        return
    
    choice = int(choice)

    # Cancel option is always the last one
    if choice == max_option:
        print("Update cancelled")
        return
    
    # Admin update options
    if user["role"] == "admin":

        # Update category
        if choice == 1 or choice == 6:
            print("\nAvailable categories: ")
            for i, cat in enumerate(categories, 1):
                print(f"  {i}. {cat} (Max: Rp{reimbursement_cap[cat]:,})")

            while True:
                category_input = input("\nNew Category (enter name or number): ")

                # Selection by number 
                if category_input.isdigit() and 1 <= int(category_input) <= len(categories):
                    found_item["category"] = categories[int(category_input) - 1]
                    break

                # Or by name
                elif validate_category(category_input):
                    found_item["category"] = category_input
                    break

        # Update amount
        if choice == 2 or choice == 6:
            while True:
                amount_str = input(f"New Amount (max Rp{reimbursement_cap[found_item['category']]:,}): ")
                amount = validate_amount(amount_str, found_item["category"])
                if amount is not None:
                    found_item["amount"] = amount
                    break

        # Update date
        if choice == 3 or choice == 6:
            while True:
                date_input = input("New Date (yyyy-mm-dd): ")
                validated_date = validate_date(date_input)
                if validated_date is not None:
                    found_item["date"] = validated_date
                    break

        # Update status
        if choice == 4 or choice == 6:
            valid_statuses = ["Under Review", "Approved", "Rejected"]
            print("\nStatus options: ")
            for i, status in enumerate(valid_statuses, 1):
                print(f"   {i}. {status}")

            while True:
                status_input = input("\nNew Status (enter name or number): ")
                if status_input.isdigit() and 1 <= int(status_input) <= len(valid_statuses):
                    found_item["status"] = valid_statuses[int(status_input) - 1]
                    break
                elif status_input in valid_statuses:
                    found_item["status"] = status_input
                    break
                else:
                    print(f"Invalid status. Please choose from {valid_statuses}")

        # Update description
        if choice == 5 or choice == 6:
            print("\nPlease provide a description for this expense (e.g, purpose, location, participants)")
            found_item["description"] = input("New Description: ")
    
    # Add audit information
    found_item["last_updated_by"] = user["username"]
    found_item["last_updated_on"] = datetime.now().strftime('%Y-%m-%d')
        
    print("Reimbursement updated successfully!")
    
def delete_reimbursement(user):
    # Only admins can delete reimbursements
    if user["role"] != "admin":
        print("\nOnly administrators can delete Reimbursements.")
        return
    
    print("\nDelete Reimbursement")
    view_reimbursements(user)

    while True:
        expense_id = input("\nEnter Expense ID to delete (or 'cancel' to go back): ")
        if expense_id.lower() == 'cancel':
            return

        # Find the reimbursement
        found_item = None
        for item in data_reimbursements:
            if item["expense_id"] == expense_id:
                found_item = item
                break

        if found_item:
            break
        print("Item not found. Please try again.")

    # Show details and confirm deletion
    print("\nReimbursement to be deleted: ")
    print(f"Expense ID: {found_item['expense_id']}")
    print(f"Employee: {found_item['name']} (ID: {found_item['employee_id']})")
    print(f"Category: {found_item['category']}")
    print(f"Amount: Rp{found_item['amount']:,}")
    print(f"Date: {found_item['date']}")
    print(f"Status: {found_item['status']}")

    # Confirmation for deletion
    print("\nWARNING: Deletion is permanent and should only be used in exceptional circumstances.")
    reason = input("Please enter reason for deletion (required): ")

    if not reason.strip():
        print("A reason is required for deletion. Operation cancelled.")
        return

    confirm = input("\nAre you sure you want to delete this reimbursement? (Y/N): ").upper()
    if confirm != 'Y':
        print("Deletion cancelled.")
        return

    # Log deletion before removing the item
    deletion_log = {
        "expense_id": found_item["expense_id"],
        "deleted_by": user["username"],
        "deleted_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reason": reason,
        "item_data": found_item.copy()              # Save copy of the deleted item
    }
    deletion_logs.append(deletion_log)
    print(f"\nDeletion logged: Expense ID {found_item['expense_id']} deleted by {user['username']}")

    # Remove the item
    data_reimbursements.remove(found_item)
    print("Reimbursement deleted successfully")

def search_reimbursements(user):
    print("\nSearch Reimbursements")
    print("1. Search by Employee")
    print("2. Search by Category")
    print("3. Search by Status")
    print("4. Search by Date Range")
    print("5. Search by Amount Range")
    print("6. Return to Main Menu")

    choice = input("\nEnter your choice (1-6): ")

    filtered_data = []

    if choice == '1':
        # Display available employees
        print("\nAvailable employees: ")
        for id, name in data_employeeID.items():
            print(f"  {id}: {name}")

        employee_id = input("\nEnter Employee ID: ")
        filtered_data = [item for item in data_reimbursements if item["employee_id"] == employee_id]

    elif choice == '2':
        # Display available categories
        print("\nAvailable categories: ")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")

        category_input = input("\nEnter category (name or number): ")
        selected_category = ""

        if category_input.isdigit() and 1 <= int(category_input) <= len(categories):
            selected_category = categories[int(category_input) - 1]

        else:
            selected_category = category_input
            
        filtered_data = [item for item in data_reimbursements if item["category"] == selected_category]

    elif choice == '3':
        valid_statuses = ["Under Review", "Approved", "Rejected"]
        print("\nStatus options:")
        for i, status in enumerate(valid_statuses, 1):
            print(f"  {i}. {status}")
            
        status_input = input("\nEnter status (name or number): ")
        selected_status = ""
        
        if status_input.isdigit() and 1 <= int(status_input) <= len(valid_statuses):
            selected_status = valid_statuses[int(status_input) - 1]
        else:
            selected_status = status_input
            
        filtered_data = [item for item in data_reimbursements if item["status"] == selected_status]
        
    elif choice == '4':
        start_date = None
        while not start_date:
            start_input = input("\nEnter start date (yyyy-mm-dd): ")
            start_date = validate_date(start_input)
            
        end_date = None
        while not end_date:
            end_input = input("Enter end date (yyyy-mm-dd): ")
            end_date = validate_date(end_input)
            
        filtered_data = [item for item in data_reimbursements if start_date <= item["date"] <= end_date]
        
    elif choice == '5':
        min_amount = None
        while min_amount is None:
            min_input = input("\nEnter minimum amount: ")
            if min_input.isdigit() and int(min_input) >= 0:
                min_amount = int(min_input)
            else:
                print("Please enter a valid positive number.")
                
        max_amount = None
        while max_amount is None:
            max_input = input("Enter maximum amount: ")
            if max_input.isdigit() and int(max_input) >= min_amount:
                max_amount = int(max_input)
            else:
                print(f"Please enter a valid number greater than or equal to {min_amount}.")
                
        filtered_data = [item for item in data_reimbursements if min_amount <= item["amount"] <= max_amount]
        
    elif choice == '6':
        return
    
    # Display results
    if not filtered_data:
        print("\nNo matching reimbursements found.")
        return
        
    print(f"\nFound {len(filtered_data)} matching reimbursements:")
    
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
    ] for item in filtered_data]

    print(tabulate(table, headers, tablefmt="grid"))

def display_menu(user):
    print("\nBusiness Reimbursement System")

    if user["role"] == "admin":
        print("1. Add Reimbursement")
        print("2. View All Reimbursements")
        print("3. Update Reimbursement")
        print("4. Delete Reimbursement")
        print("5. Search & Filter Reimbursements")
        print("6. Exit")
        return 6  # Return the number of options
    
    elif user["role"] == "manager":
        print("1. Add Reimbursement")
        print("2. View All Reimbursements")
        print("3. Approve/Reject Reimbursement")
        print("4. Search & Filter Reimbursements")
        print("5. Exit")
        return 5  
    
    else:
        print("1. Add New Reimbursement")
        print("2. View My Reimbursements")
        print("3. Update My Pending Reimbursement")
        print("4. Exit")
        return 4  

def main():
    current_user = login()
    if not current_user:
        return

    while True:
        max_options = display_menu(current_user)
        choice = input(f"\nEnter your choice (1-{max_options}): ")

        if not choice.isdigit() or int(choice) < 1 or int(choice) > max_options:
            print("Invalid choice. Please try again.")
            continue

        choice = int(choice)

        if current_user["role"] == "admin":
            if choice == 1:
                add_reimbursement(current_user)
            elif choice == 2:
                view_reimbursements(current_user)
            elif choice == 3:
                update_reimbursement(current_user)
            elif choice == 4:
                delete_reimbursement(current_user)
            elif choice == 5:
                search_reimbursements(current_user)
            elif choice == 6:
                print("Exiting the system.")
                break

        elif current_user["role"] == "manager":
            if choice == 1:
                add_reimbursement(current_user)
            elif choice == 2:
                view_reimbursements(current_user)
            elif choice == 3:
                approve_reimbursement(current_user)
            elif choice == 4:
                search_reimbursements(current_user)
            elif choice == 5:
                print("Exiting the system.")
                break

        else:       # Employee
            if choice == 1:
                add_reimbursement(current_user)
            elif choice == 2:
                view_reimbursements(current_user)
            elif choice == 3:
                update_reimbursement(current_user)
            elif choice == 4:
                print("Exiting the system.")
                break

# Run the program
main() 