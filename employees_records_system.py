# Imports for graphical charts
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# In-memory employee data (resets when program exits)
employees = [
    {"id": 1, "name": "Alice", "department": "Engineering", "tickets": 18},
    {"id": 2, "name": "Brian", "department": "Engineering", "tickets": 12},
    {"id": 3, "name": "Carla", "department": "Support", "tickets": 25},
    {"id": 4, "name": "David2", "department": "Support", "tickets": 9},
    {"id": 5, "name": "Emily", "department": "Compliance", "tickets": 14},
    {"id": 6, "name": "Frank", "department": "Security", "tickets": 7},
    {"id": 7, "name": "Grace", "department": "Security", "tickets": 20},
    {"id": 8, "name": "Henry", "department": "Marketing", "tickets": 11},
]

# Valid departments list
DEPARTMENTS = ["Engineering", "Support", "Compliance", "Security", "Marketing"]

# Tracks the next available ID for new employees
next_id = 9


def get_next_id():  # Returns next ID and increments the counter
    global next_id
    current = next_id
    next_id += 1
    return current


# Max width of terminal bar chart bars
BAR_WIDTH = 30

# Unicode symbols for each department in terminal chart
DEPT_SYMBOLS = {
    "Engineering": "█",
    "Support":     "▓",
    "Compliance":  "░",
    "Security":    "▒",
    "Marketing":   "▞",
}

import colorsys  # Built-in module for color conversions (HSL to RGB)


# Base HSL colors per department for matplotlib chart
DEPT_BASE_COLORS = {
    "Engineering": (0.58, 0.85, 0.70),
    "Support":     (0.33, 0.85, 0.70),
    "Compliance":  (0.75, 0.65, 0.70),
    "Security":    (0.00, 0.80, 0.70),
    "Marketing":   (0.08, 0.85, 0.70),
}


def generate_palette(dept, count):  # Creates shade variations for employees in same department
    base_h, base_s, base_l = DEPT_BASE_COLORS.get(dept, (0.0, 0.0, 0.60))
    if count == 1:
        r, g, b = colorsys.hls_to_rgb(base_h, base_l, base_s)
        return [f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"]
    colors = []
    for i in range(count):
        lightness = base_l - 0.20 + (0.40 * i / (count - 1))
        lightness = max(0.25, min(0.90, lightness))
        saturation = base_s - (0.15 * i / (count - 1))
        saturation = max(0.30, min(1.0, saturation))
        r, g, b = colorsys.hls_to_rgb(base_h, lightness, saturation)
        colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
    return colors


def get_employee_color(emp):  # Assigns a unique shade to each employee based on dept rank
    dept = emp["department"]
    dept_employees = sorted(
        [e for e in employees if e["department"] == dept],
        key=lambda e: e["tickets"], reverse=True,
    )
    palette = generate_palette(dept, len(dept_employees))
    idx = next((i for i, e in enumerate(dept_employees) if e["id"] == emp["id"]), 0)
    return palette[idx]


def show_terminal_chart(records, title="Employee Weekly Metrics"):  # Prints horizontal bar chart in terminal
    if not records:
        print("\nNo records to chart.")
        return
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True)
    max_tickets = max(e["tickets"] for e in sorted_records)
    max_name = max(len(e["name"]) for e in sorted_records)

    print(f"\n  {title}")
    print(f"  {'=' * (max_name + BAR_WIDTH + 12)}")

    for emp in sorted_records:
        bar_len = int((emp["tickets"] / max_tickets) * BAR_WIDTH) if max_tickets > 0 else 0
        symbol = DEPT_SYMBOLS.get(emp["department"], "█")
        bar = symbol * bar_len
        print(f"  {emp['name']:<{max_name}}  |{bar:<{BAR_WIDTH}}| {emp['tickets']}")

    print()
    legend = "  Legend: " + "  ".join(
        f"{sym} {dept}" for dept, sym in DEPT_SYMBOLS.items()
        if any(e["department"] == dept for e in sorted_records)
    )
    print(legend)
    print()


def show_matplotlib_chart(records, title="Employee Weekly Metrics"):  # Opens graphical bar chart window
    if not records:
        return
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True)
    names = [e["name"] for e in sorted_records]
    tickets = [e["tickets"] for e in sorted_records]
    colors = [get_employee_color(e) for e in sorted_records]

    fig, ax = plt.subplots(figsize=(10, max(4, len(names) * 0.6)))
    bars = ax.barh(names[::-1], tickets[::-1], color=colors[::-1], edgecolor="#333333", linewidth=0.5)

    for bar, count in zip(bars, tickets[::-1]):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                str(count), va="center", fontweight="bold", fontsize=9)

    ax.set_xlabel("Tickets Completed", fontsize=11)
    ax.set_title(title, fontsize=13, fontweight="bold")

    legend_handles = [
        mpatches.Patch(color=generate_palette(dept, 1)[0], label=dept)
        for dept in DEPARTMENTS
        if any(e["department"] == dept for e in sorted_records)
    ]
    ax.legend(handles=legend_handles, loc="lower right", fontsize=9)

    plt.tight_layout()
    plt.show()


def show_bar_chart(records, title="Employee Weekly Metrics"):  # Shows terminal chart, optionally opens graphical one
    show_terminal_chart(records, title)
    open_chart = input("Open graphical chart? (y/n): ").strip().lower() # Prompt user to open matplotlib chart after showing terminal version
    if open_chart == "y":
        show_matplotlib_chart(records, title)


def display_records(records):  # Prints formatted table ranked by tickets (highest first)
    if not records:
        print("\nNo records found.")
        return
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True) # Sorts employees by tickets in descending order for display
    print(f"\n{'Rank':<6}{'ID':<6}{'Name':<22}{'Department':<16}{'Tickets':<8}")
    print("-" * 58)
    for rank, emp in enumerate(sorted_records, start=1):
        print(f"{rank:<6}{emp['id']:<6}{emp['name']:<22}{emp['department']:<16}{emp['tickets']:<8}")


def view_all():  # Displays all employees + chart
    print("\n===== All Employee Weekly Records (Highest to Lowest) =====")
    display_records(employees)
    show_bar_chart(employees, "All Employees - Weekly Metrics")


def view_by_department():  # Filters and displays employees by department
    print("\nDepartments:", ", ".join(DEPARTMENTS))
    dept = input("Enter department name: ").strip()
    matched = [e for e in employees if e["department"].lower() == dept.lower()]
    if not matched:
        print(f"No employees found in '{dept}'. Check the department name.")
        return
    print(f"\n===== {dept} - Weekly Records (Highest to Lowest) =====")
    display_records(matched)
    show_bar_chart(matched, f"{dept} - Weekly Metrics")


def create_employee():  # Adds new employee with validation (name, dept, duplicates, tickets)
    name = input("Enter username (letters and numbers only, no spaces): ").strip()
    if not name:
        print("Username cannot be empty.")
        return
    if not name.isalnum():
        print("Username must be plain text only (letters and numbers, no spaces or special characters).")
        return

    print("Departments:", ", ".join(DEPARTMENTS))
    dept = input("Enter department: ").strip()
    if dept not in DEPARTMENTS:
        print(f"Invalid department. Choose from: {', '.join(DEPARTMENTS)}")
        return

    duplicate = any(
        e for e in employees
        if e["name"].lower() == name.lower() and e["department"].lower() == dept.lower()
    )
    if duplicate:
        print(f"An employee named '{name}' already exists in {dept}.")
        return

    try:
        tickets = int(input("Enter number of tickets completed this week: "))
        if tickets < 0:
            print("Tickets cannot be negative.")
            return
    except ValueError:
        print("Invalid number.")
        return

    new_id = get_next_id()
    employees.append({"id": new_id, "name": name, "department": dept, "tickets": tickets})
    print(f"Employee '{name}' added with ID {new_id}.")


def update_employee():  # Edits existing employee by ID (blank input keeps current value)
    try:
        emp_id = int(input("Enter employee ID to update: "))
    except ValueError:
        print("Invalid ID.")
        return

    emp = next((e for e in employees if e["id"] == emp_id), None)
    if not emp:
        print(f"No employee found with ID {emp_id}.")
        return

    print(f"Current record: {emp['name']} | {emp['department']} | Tickets: {emp['tickets']}")
    print("Leave a field blank to keep the current value.\n")

    name = input(f"New username [{emp['name']}]: ").strip()
    if name:
        if not name.isalnum(): 
            print("Username must be plain text only (letters and numbers, no spaces or special characters). Keeping current value.")
        else:
            emp["name"] = name

    print("Departments:", ", ".join(DEPARTMENTS))
    dept = input(f"New department [{emp['department']}]: ").strip()
    if dept:
        if dept not in DEPARTMENTS:
            print(f"Invalid department. Keeping '{emp['department']}'.")
        else:
            emp["department"] = dept

    tickets_input = input(f"New ticket count [{emp['tickets']}]: ").strip()
    if tickets_input:
        try:
            tickets = int(tickets_input)
            if tickets < 0:
                print("Tickets cannot be negative. Keeping current value.")
            else:
                emp["tickets"] = tickets
        except ValueError:
            print("Invalid number. Keeping current ticket count.")

    print(f"Employee ID {emp_id} updated.")


def delete_employee():  # Removes employee by ID with confirmation prompt
    try:
        emp_id = int(input("Enter employee ID to delete: "))
    except ValueError:
        print("Invalid ID.")
        return

    emp = next((e for e in employees if e["id"] == emp_id), None)
    if not emp:
        print(f"No employee found with ID {emp_id}.")
        return

    confirm = input(f"Delete '{emp['name']}' from {emp['department']}? (y/n): ").strip().lower()
    if confirm == "y":
        employees.remove(emp)
        print(f"Employee '{emp['name']}' deleted.")
    else:
        print("Delete cancelled.")


def main():  # Main menu loop — routes user input to CRUD and view functions
    menu = """
========================================
   Employees Records System
========================================
1. View all records
2. View by department
3. Add employee
4. Update employee
5. Delete employee
6. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option (1-6): ").strip()

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
            print("See you next time!")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
