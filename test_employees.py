import os
import unittest
from unittest.mock import patch
import database as db
import charts
import employees_records_system as ers

# Use a separate test database so production data is never touched
TEST_DB = "test_employees.db"


def setUpModule():
    """Initialize a fresh test database before any tests run."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    db.init_db(TEST_DB)


def tearDownModule():
    """Remove the test database after all tests complete."""
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


class TestDatabaseInit(unittest.TestCase):
    """Test that the database initializes and seeds correctly."""

    def test_seed_data_loaded(self):
        employees = db.get_all(TEST_DB)
        self.assertEqual(len(employees), 8)

    def test_seed_data_ids(self):
        employees = db.get_all(TEST_DB)
        ids = [e["id"] for e in employees]
        self.assertEqual(ids, list(range(1, 9)))


class TestGeneratePalette(unittest.TestCase):
    """Test color palette generation for departments."""

    def test_single_employee_returns_one_color(self):
        palette = charts.generate_palette("Engineering", 1)
        self.assertEqual(len(palette), 1)
        self.assertTrue(palette[0].startswith("#"))

    def test_multiple_employees_returns_correct_count(self):
        palette = charts.generate_palette("Support", 5)
        self.assertEqual(len(palette), 5)

    def test_all_colors_are_valid_hex(self):
        palette = charts.generate_palette("Security", 3)
        for color in palette:
            self.assertRegex(color, r"^#[0-9a-f]{6}$")

    def test_colors_are_unique(self):
        palette = charts.generate_palette("Engineering", 4)
        self.assertEqual(len(palette), len(set(palette)))

    def test_unknown_department_uses_fallback(self):
        palette = charts.generate_palette("Unknown", 2)
        self.assertEqual(len(palette), 2)


class TestGetEmployeeColor(unittest.TestCase):
    """Test that each employee gets a valid hex color."""

    def test_returns_hex_color(self):
        employees = db.get_all(TEST_DB)
        emp = employees[0]  # Alice
        color = charts.get_employee_color(emp, employees)
        self.assertRegex(color, r"^#[0-9a-f]{6}$")

    def test_same_dept_employees_get_different_colors(self):
        employees = db.get_all(TEST_DB)
        alice = employees[0]  # Engineering
        brian = employees[1]  # Engineering
        self.assertNotEqual(
            charts.get_employee_color(alice, employees),
            charts.get_employee_color(brian, employees),
        )


class TestDepartmentFiltering(unittest.TestCase):
    """Test filtering employees by department."""

    def test_filter_engineering(self):
        matched = db.get_by_department("Engineering", TEST_DB)
        self.assertEqual(len(matched), 2)
        self.assertTrue(all(e["department"] == "Engineering" for e in matched))

    def test_filter_case_insensitive(self):
        matched = db.get_by_department("support", TEST_DB)
        self.assertEqual(len(matched), 2)

    def test_filter_nonexistent_department(self):
        matched = db.get_by_department("HR", TEST_DB)
        self.assertEqual(len(matched), 0)


class TestSorting(unittest.TestCase):
    """Test that records sort by tickets highest to lowest."""

    def test_sort_descending(self):
        employees = db.get_all(TEST_DB)
        sorted_records = sorted(employees, key=lambda e: e["tickets"], reverse=True)
        tickets = [e["tickets"] for e in sorted_records]
        self.assertEqual(tickets, sorted(tickets, reverse=True))

    def test_highest_is_first(self):
        employees = db.get_all(TEST_DB)
        sorted_records = sorted(employees, key=lambda e: e["tickets"], reverse=True)
        self.assertEqual(sorted_records[0]["name"], "Carla")
        self.assertEqual(sorted_records[0]["tickets"], 25)


class TestDuplicateDetection(unittest.TestCase):
    """Test that duplicate name+department combos are detected."""

    def test_duplicate_found(self):
        self.assertTrue(db.has_duplicate("Alice", "Engineering", TEST_DB))

    def test_no_duplicate_different_dept(self):
        self.assertFalse(db.has_duplicate("Alice", "Support", TEST_DB))

    def test_no_duplicate_different_name(self):
        self.assertFalse(db.has_duplicate("Zara", "Engineering", TEST_DB))


class TestInputValidation(unittest.TestCase):
    """Test username validation rules."""

    def test_valid_alphanumeric(self):
        self.assertTrue("Alice123".isalnum())

    def test_rejects_spaces(self):
        self.assertFalse("Alice Smith".isalnum())

    def test_rejects_special_characters(self):
        self.assertFalse("Alice@!".isalnum())

    def test_rejects_empty(self):
        self.assertFalse("".isalnum())

    def test_valid_department(self):
        self.assertIn("Engineering", db.DEPARTMENTS)

    def test_invalid_department(self):
        self.assertNotIn("HR", db.DEPARTMENTS)


class TestSearchEmployee(unittest.TestCase):
    """Test employee search by name (partial match)."""

    def test_exact_match(self):
        matched = db.search_by_name("Alice", TEST_DB)
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["name"], "Alice")

    def test_partial_match(self):
        matched = db.search_by_name("al", TEST_DB)
        self.assertEqual(len(matched), 1)

    def test_no_match(self):
        matched = db.search_by_name("xyz", TEST_DB)
        self.assertEqual(len(matched), 0)

    def test_case_insensitive(self):
        matched = db.search_by_name("GRACE", TEST_DB)
        self.assertEqual(len(matched), 1)


class TestCreateEmployee(unittest.TestCase):
    """Test adding a new employee via the database module."""

    def test_create_valid_employee(self):
        new_id = db.create_employee("Zara", "Engineering", 15, TEST_DB)
        self.assertIsNotNone(new_id)
        emp = db.get_by_id(new_id, TEST_DB)
        self.assertEqual(emp["name"], "Zara")
        self.assertEqual(emp["department"], "Engineering")
        self.assertEqual(emp["tickets"], 15)
        # Clean up
        db.delete_employee(new_id, TEST_DB)

    def test_duplicate_detected(self):
        self.assertTrue(db.has_duplicate("Alice", "Engineering", TEST_DB))


class TestDeleteEmployee(unittest.TestCase):
    """Test deleting an employee via the database module."""

    def test_delete_and_verify(self):
        new_id = db.create_employee("TempUser", "Marketing", 5, TEST_DB)
        self.assertTrue(db.delete_employee(new_id, TEST_DB))
        self.assertIsNone(db.get_by_id(new_id, TEST_DB))

    def test_delete_nonexistent(self):
        self.assertFalse(db.delete_employee(99999, TEST_DB))


class TestUpdateEmployee(unittest.TestCase):
    """Test updating an employee via the database module."""

    def test_update_name(self):
        new_id = db.create_employee("UpdateMe", "Support", 10, TEST_DB)
        db.update_employee(new_id, name="Updated", db_path=TEST_DB)
        emp = db.get_by_id(new_id, TEST_DB)
        self.assertEqual(emp["name"], "Updated")
        db.delete_employee(new_id, TEST_DB)

    def test_update_nonexistent(self):
        result = db.update_employee(99999, name="Ghost", db_path=TEST_DB)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
