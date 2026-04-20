"""Employee Records System - Main application module.

Provides the interactive CLI menu for managing employee records.
Uses SQLite for persistent storage (via database module) and
charts module for data visualization.
"""

import database as db                # Database module — handles all SQLite read/write operations
from database import DEPARTMENTS     # List of valid department names shared across modules
from charts import show_bar_chart    # Chart function — shows terminal + optional matplotlib chart


def display_records(records):
    """Print a formatted table of employees ranked by tickets (highest first).

    Args:
        records: List of employee dicts to display.
    """
    if not records:
        print("\nNo records found.")
        return
    # Sort employees by tickets descending so highest performers appear first
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True)
    print(f"\n{'Rank':<6}{'ID':<6}{'Name':<22}{'Department':<16}{'Tickets':<8}")
    print("-" * 58)
    for rank, emp in enumerate(sorted_records, start=1):  # enumerate starts at 1 for display ranking
        print(f"{rank:<6}{emp['id']:<6}{emp['name']:<22}{emp['department']:<16}{emp['tickets']:<8}")


def view_all():
    """Display all employees in a ranked table and bar chart."""
    employees = db.get_all()
    print("\n===== All Employee Weekly Records (Highest to Lowest) =====")
    display_records(employees)
    show_bar_chart(employees, "All Employees - Weekly Metrics")


def view_by_department():
    """Prompt for a department name, then display its employees and chart."""
    print("\nDepartments:", ", ".join(DEPARTMENTS))
    dept = input("Enter department name: ").strip()
    matched = db.get_by_department(dept)
    if not matched:
        print(f"No employees found in '{dept}'. Check the department name.")
        return
    print(f"\n===== {dept} - Weekly Records (Highest to Lowest) =====")
    display_records(matched)
    show_bar_chart(matched, f"{dept} - Weekly Metrics")


def create_employee():
    """Add a new employee with validation for name, department, duplicates, and tickets."""
    name = input("Enter username (letters and numbers only, no spaces): ").strip()
    if not name:
        print("Username cannot be empty.")
        return
    if not name.isalnum():  # isalnum() rejects spaces, symbols, and empty strings
        print("Username must be plain text only (letters and numbers, no spaces or special characters).")
        return

    print("Departments:", ", ".join(DEPARTMENTS))
    dept = input("Enter department: ").strip()
    if dept not in DEPARTMENTS:  # Must match one of the predefined departments exactly
        print(f"Invalid department. Choose from: {', '.join(DEPARTMENTS)}")
        return
    if db.has_duplicate(name, dept):  # Check database for same name + department combo
        print(f"An employee named '{name}' already exists in {dept}.")
        return

    try:
        tickets = int(input("Enter number of tickets completed this week: "))  # Convert string input to integer
        if tickets < 0:
            print("Tickets cannot be negative.")
            return
    except ValueError:
        print("Invalid number.")
        return

    new_id = db.create_employee(name, dept, tickets)  # Insert into SQLite, returns auto-generated ID
    print(f"Employee '{name}' added with ID {new_id}.")


def update_employee():
    """Edit an existing employee by ID. Blank input keeps the current value."""
    try:
        emp_id = int(input("Enter employee ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    emp = db.get_by_id(emp_id)
    if not emp:
        print(f"No employee found with ID {emp_id}.")
        return

    print(f"Current record: {emp['name']} | {emp['department']} | Tickets: {emp['tickets']}")
    print("Leave a field blank to keep the current value.\n")

    # None means "don't change this field" — only non-None values get written to the database
    new_name = None
    name = input(f"New username [{emp['name']}]: ").strip()
    if name:
        if not name.isalnum():
            print("Username must be plain text only (letters and numbers, no spaces or special characters). Keeping current value.")
        else:
            new_name = name

    new_dept = None
    print("Departments:", ", ".join(DEPARTMENTS))
    dept = input(f"New department [{emp['department']}]: ").strip()
    if dept:
        if dept not in DEPARTMENTS:
            print(f"Invalid department. Keeping '{emp['department']}'.")
        else:
            new_dept = dept

    new_tickets = None
    tickets_input = input(f"New ticket count [{emp['tickets']}]: ").strip()
    if tickets_input:
        try:
            tickets = int(tickets_input)
            if tickets < 0:
                print("Tickets cannot be negative. Keeping current value.")
            else:
                new_tickets = tickets
        except ValueError:
            print("Invalid number. Keeping current ticket count.")

    # Pass only changed fields — None values are ignored by the database function
    db.update_employee(emp_id, name=new_name, department=new_dept, tickets=new_tickets)
    print(f"Employee ID {emp_id} updated.")


def delete_employee():
    """Remove an employee by ID with a confirmation prompt."""
    try:
        emp_id = int(input("Enter employee ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    emp = db.get_by_id(emp_id)
    if not emp:
        print(f"No employee found with ID {emp_id}.")
        return

    confirm = input(f"Delete '{emp['name']}' from {emp['department']}? (y/n): ").strip().lower()
    if confirm == "y":
        db.delete_employee(emp_id)
        print(f"Employee '{emp['name']}' deleted.")
    else:
        print("Delete cancelled.")


def search_employee():
    """Search employees by name using partial, case-insensitive matching."""
    name = input("Enter name to search: ").strip()
    if not name:
        print("Search term cannot be empty.")
        return
    matched = db.search_by_name(name)
    if not matched:
        print(f"No employees found matching '{name}'.")
        return
    print(f"\n===== Search Results for '{name}' =====")
    display_records(matched)


def main():
    """Main menu loop — initializes the database and routes user input to CRUD functions."""
    db.init_db()  # Create tables and seed data on first run; no-op if database already exists
    menu = """
========================================
   Employees Records System
========================================
1. View all records
2. View by department
3. Add employee
4. Update employee
5. Delete employee
6. Search employee by name
7. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            view_all()
        elif choice == "2":
            view_by_department()
        elif choice == "3":
            create_employee()
        elif choice == "4":
            update_employee()
        elif choice == "5":
            delete_employee()
        elif choice == "6":
            search_employee()
        elif choice == "7":
            print("See you next time!")
            break
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()
