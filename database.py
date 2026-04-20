"""SQLite database module for the Employee Records System.

Handles database initialization, seeding, and all CRUD operations
for employee records. Uses an SQLite database file (employees.db)
for persistent storage.
"""

import sqlite3  # Python's built-in module for SQLite database operations

# Valid departments list
DEPARTMENTS = ["Engineering", "Support", "Compliance", "Security", "Marketing"]

# Default database file path
DB_PATH = "employees.db"

# Seed data used when initializing a fresh database
SEED_DATA = [
    (1, "Alice", "Engineering", 18),
    (2, "Brian", "Engineering", 12),
    (3, "Carla", "Support", 25),
    (4, "David2", "Support", 9),
    (5, "Emily", "Compliance", 14),
    (6, "Frank", "Security", 7),
    (7, "Grace", "Security", 20),
    (8, "Henry", "Marketing", 11),
]


def get_connection(db_path=None):
    """Return a new SQLite connection to the database.

    Args:
        db_path: Optional path to the database file. Defaults to DB_PATH.

    Returns:
        A sqlite3.Connection with row_factory set to sqlite3.Row.
    """
    conn = sqlite3.connect(db_path or DB_PATH)  # Opens the .db file (creates it if it doesn't exist)
    conn.row_factory = sqlite3.Row  # Lets us access columns by name like row["name"] instead of row[0]
    return conn


def init_db(db_path=None):
    """Create the employees table and seed it with initial data if empty.

    Args:
        db_path: Optional path to the database file. Defaults to DB_PATH.
    """
    conn = get_connection(db_path)
    try:
        # Create the table if it doesn't already exist (safe to run multiple times)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                tickets INTEGER NOT NULL DEFAULT 0
            )
        """)
        # Only seed data if the table is empty (first-time setup)
        row = conn.execute("SELECT COUNT(*) AS cnt FROM employees").fetchone()
        if row["cnt"] == 0:
            conn.executemany(
                "INSERT INTO employees (id, name, department, tickets) VALUES (?, ?, ?, ?)",
                SEED_DATA,
            )
        conn.commit()  # Save changes to disk
    finally:
        conn.close()  # Always close the connection to free resources


def _row_to_dict(row):
    """Convert a sqlite3.Row to a plain dictionary.

    Args:
        row: A sqlite3.Row object.

    Returns:
        A dict with keys: id, name, department, tickets.
    """
    return {"id": row["id"], "name": row["name"],
            "department": row["department"], "tickets": row["tickets"]}


def get_all(db_path=None):
    """Retrieve all employee records from the database.

    Args:
        db_path: Optional path to the database file.

    Returns:
        A list of dicts, each representing an employee.
    """
    conn = get_connection(db_path)
    try:
        rows = conn.execute("SELECT * FROM employees ORDER BY id").fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def get_by_department(department, db_path=None):
    """Retrieve employees belonging to a specific department.

    Args:
        department: Department name (case-insensitive match).
        db_path: Optional path to the database file.

    Returns:
        A list of employee dicts in that department.
    """
    conn = get_connection(db_path)
    try:
        # COLLATE NOCASE makes the match case-insensitive ("support" matches "Support")
        # The ? placeholder prevents SQL injection by safely passing user input
        rows = conn.execute(
            "SELECT * FROM employees WHERE department = ? COLLATE NOCASE ORDER BY id",
            (department,),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def get_by_id(emp_id, db_path=None):
    """Retrieve a single employee by their ID.

    Args:
        emp_id: The integer ID of the employee.
        db_path: Optional path to the database file.

    Returns:
        An employee dict, or None if not found.
    """
    conn = get_connection(db_path)
    try:
        row = conn.execute("SELECT * FROM employees WHERE id = ?", (emp_id,)).fetchone()
        return _row_to_dict(row) if row else None
    finally:
        conn.close()


def search_by_name(name, db_path=None):
    """Search for employees whose name contains the given string.

    Args:
        name: Partial name to search for (case-insensitive).
        db_path: Optional path to the database file.

    Returns:
        A list of matching employee dicts.
    """
    conn = get_connection(db_path)
    try:
        # LIKE with %name% matches any name containing the search term
        rows = conn.execute(
            "SELECT * FROM employees WHERE name LIKE ? COLLATE NOCASE ORDER BY id",
            (f"%{name}%",),
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    finally:
        conn.close()


def has_duplicate(name, department, db_path=None):
    """Check if an employee with the same name and department already exists.

    Args:
        name: Employee name to check.
        department: Department to check.
        db_path: Optional path to the database file.

    Returns:
        True if a duplicate exists, False otherwise.
    """
    conn = get_connection(db_path)
    try:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM employees WHERE name = ? COLLATE NOCASE AND department = ? COLLATE NOCASE",
            (name, department),
        ).fetchone()
        return row["cnt"] > 0
    finally:
        conn.close()


def create_employee(name, department, tickets, db_path=None):
    """Insert a new employee record into the database.

    Args:
        name: Employee name (alphanumeric).
        department: Department name (must be in DEPARTMENTS).
        tickets: Number of tickets completed (non-negative integer).
        db_path: Optional path to the database file.

    Returns:
        The new employee's auto-generated ID.
    """
    conn = get_connection(db_path)
    try:
        # ? placeholders prevent SQL injection — never use f-strings in SQL queries
        cursor = conn.execute(
            "INSERT INTO employees (name, department, tickets) VALUES (?, ?, ?)",
            (name, department, tickets),
        )
        conn.commit()  # Save the new record to disk
        return cursor.lastrowid  # SQLite auto-generates the ID via AUTOINCREMENT
    finally:
        conn.close()


def update_employee(emp_id, name=None, department=None, tickets=None, db_path=None):
    """Update fields of an existing employee record.

    Only non-None arguments will be updated. Pass None to keep current value.

    Args:
        emp_id: The ID of the employee to update.
        name: New name, or None to keep current.
        department: New department, or None to keep current.
        tickets: New ticket count, or None to keep current.
        db_path: Optional path to the database file.

    Returns:
        True if the employee was found and updated, False otherwise.
    """
    emp = get_by_id(emp_id, db_path)
    if not emp:
        return False

    # Keep current value for any field the user didn't change (passed as None)
    new_name = name if name is not None else emp["name"]
    new_dept = department if department is not None else emp["department"]
    new_tickets = tickets if tickets is not None else emp["tickets"]

    conn = get_connection(db_path)
    try:
        conn.execute(
            "UPDATE employees SET name = ?, department = ?, tickets = ? WHERE id = ?",
            (new_name, new_dept, new_tickets, emp_id),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def delete_employee(emp_id, db_path=None):
    """Delete an employee record by ID.

    Args:
        emp_id: The ID of the employee to delete.
        db_path: Optional path to the database file.

    Returns:
        True if the employee was found and deleted, False otherwise.
    """
    conn = get_connection(db_path)
    try:
        cursor = conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        return cursor.rowcount > 0  # rowcount is 0 if no row matched the ID
    finally:
        conn.close()
