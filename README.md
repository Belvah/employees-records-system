# Employees Records System

A command-line Python application that tracks weekly ticket completions per employee, with full CRUD operations and dual chart visualizations (terminal + matplotlib).

## Features

- **View all records** — Ranked table and bar chart of all employees sorted by tickets completed (highest to lowest).
- **View by department** — Filter and visualize records for a specific department.
- **Add employee** — Add a new employee with a username, department, and weekly ticket count. IDs are auto-assigned.
- **Update employee** — Modify an existing employee's username, department, or ticket count by ID. Leave a field blank to keep its current value.
- **Delete employee** — Remove an employee by ID (with confirmation prompt).
- **Dual chart display** — A text-based bar chart always prints in the terminal. You are then prompted to optionally open a color-coded matplotlib graphical chart.
- **Dynamic color palettes** — Each department gets unique shades per employee in the matplotlib chart. Colors never collide within the same department, no matter how many employees are added.

## Validation Rules

- **Username** must be a single word containing only letters and numbers (no spaces or special characters).
- **Duplicate prevention** — Cannot add an employee with the same username in the same department (case-insensitive).
- **Tickets** must be a non-negative integer.
- **Department** must be one of the predefined departments.

## Departments

- Engineering
- Support
- Compliance
- Security
- Marketing

## Requirements

- Python 3.6+
- [matplotlib](https://matplotlib.org/)

## Installation

```bash
pip install matplotlib
```

## Usage

```bash
python employees_records_system.py
```

You will see a numbered menu:

```
========================================
   Employees Records System
========================================
1. View all records
2. View by department
3. Add employee
4. Update employee
5. Delete employee
6. Exit
```

Enter the number corresponding to the action you want to perform and follow the prompts.

### Terminal Chart

When viewing records, a text-based bar chart is printed directly in the terminal using block characters:

```
  All Employees - Weekly Metrics
  =====================================================
  Carla   |▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓| 25
  Grace   |▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒          | 20
  Alice   |████████████████████████████                | 18
  Emily   |░░░░░░░░░░░░░░░░░░░░░░                      | 14
  Brian   |███████████████████                          | 12
  Henry   |▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞▞                           | 11
  David2  |▓▓▓▓▓▓▓▓▓▓▓▓▓▓                              |  9
  Frank   |▒▒▒▒▒▒▒▒▒▒▒                                  |  7

  Legend: █ Engineering  ▓ Support  ░ Compliance  ▒ Security  ▞ Marketing
```

You are then asked `Open graphical chart? (y/n):` — type `y` to open a matplotlib window, or `n` to return to the menu.

### Example: Adding an Employee

```
Choose an option (1-6): 3
Enter username (letters and numbers only, no spaces): Zara
Departments: Engineering, Support, Compliance, Security, Marketing
Enter department: Engineering
Enter number of tickets completed this week: 15
Employee 'Zara' added with ID 9.
```

### Example: Duplicate Rejected

```
Choose an option (1-6): 3
Enter username (letters and numbers only, no spaces): Alice
Departments: Engineering, Support, Compliance, Security, Marketing
Enter department: Engineering
An employee named 'Alice' already exists in Engineering.
```

## Contributing

Contributions are welcome! To get started:

1. **Fork** the repository.
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/employee_weekly.git
   cd employee_weekly
   ```
3. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them locally:
   ```bash
   python employees_records_system.py
   ```
5. **Commit** with a clear message:
   ```bash
   git add .
   git commit -m "Add: brief description of your change"
   ```
6. **Push** to your fork and open a **Pull Request**.

### Ideas for Contributions

- Persist data to a file or database so records survive between sessions.
- Add CSV/JSON export for reports.
- Add search functionality to find employees by name.
- Add unit tests.
- Support custom departments via configuration.

## Contact

For questions, suggestions, or bug reports:

- **GitHub** — [Belvah](https://github.com/Belvah)
- **GitHub Issues** — Open an issue on this repository.
- **Email** — misshuey3@gmail.com

## Notes

- Data is stored **in memory only**. All changes are lost when the program exits.
- The application ships with 8 sample employees across the five departments.
- When viewing the matplotlib chart, close the chart window to return to the menu.
