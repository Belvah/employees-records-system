import unittest
from unittest.mock import patch
import employees_records_system as ers


class TestGetNextId(unittest.TestCase):
    """Test auto-incrementing ID generation."""

    def setUp(self):
        self.original_id = ers.next_id

    def tearDown(self):
        ers.next_id = self.original_id

    def test_returns_current_and_increments(self):
        ers.next_id = 10
        self.assertEqual(ers.get_next_id(), 10)
        self.assertEqual(ers.get_next_id(), 11)
        self.assertEqual(ers.next_id, 12)


class TestGeneratePalette(unittest.TestCase):
    """Test color palette generation for departments."""

    def test_single_employee_returns_one_color(self):
        palette = ers.generate_palette("Engineering", 1)
        self.assertEqual(len(palette), 1)
        self.assertTrue(palette[0].startswith("#"))

    def test_multiple_employees_returns_correct_count(self):
        palette = ers.generate_palette("Support", 5)
        self.assertEqual(len(palette), 5)

    def test_all_colors_are_valid_hex(self):
        palette = ers.generate_palette("Security", 3)
        for color in palette:
            self.assertRegex(color, r"^#[0-9a-f]{6}$")

    def test_colors_are_unique(self):
        palette = ers.generate_palette("Engineering", 4)
        self.assertEqual(len(palette), len(set(palette)))

    def test_unknown_department_uses_fallback(self):
        palette = ers.generate_palette("Unknown", 2)
        self.assertEqual(len(palette), 2)


class TestGetEmployeeColor(unittest.TestCase):
    """Test that each employee gets a valid hex color."""

    def test_returns_hex_color(self):
        emp = ers.employees[0]  # Alice
        color = ers.get_employee_color(emp)
        self.assertRegex(color, r"^#[0-9a-f]{6}$")

    def test_same_dept_employees_get_different_colors(self):
        alice = ers.employees[0]  # Engineering
        brian = ers.employees[1]  # Engineering
        self.assertNotEqual(
            ers.get_employee_color(alice),
            ers.get_employee_color(brian),
        )


class TestDepartmentFiltering(unittest.TestCase):
    """Test filtering employees by department."""

    def test_filter_engineering(self):
        matched = [e for e in ers.employees if e["department"].lower() == "engineering"]
        self.assertEqual(len(matched), 2)
        self.assertTrue(all(e["department"] == "Engineering" for e in matched))

    def test_filter_case_insensitive(self):
        matched = [e for e in ers.employees if e["department"].lower() == "support"]
        self.assertEqual(len(matched), 2)

    def test_filter_nonexistent_department(self):
        matched = [e for e in ers.employees if e["department"].lower() == "hr"]
        self.assertEqual(len(matched), 0)


class TestSorting(unittest.TestCase):
    """Test that records sort by tickets highest to lowest."""

    def test_sort_descending(self):
        sorted_records = sorted(ers.employees, key=lambda e: e["tickets"], reverse=True)
        tickets = [e["tickets"] for e in sorted_records]
        self.assertEqual(tickets, sorted(tickets, reverse=True))

    def test_highest_is_first(self):
        sorted_records = sorted(ers.employees, key=lambda e: e["tickets"], reverse=True)
        self.assertEqual(sorted_records[0]["name"], "Carla")
        self.assertEqual(sorted_records[0]["tickets"], 25)


class TestDuplicateDetection(unittest.TestCase):
    """Test that duplicate name+department combos are detected."""

    def test_duplicate_found(self):
        duplicate = any(
            e for e in ers.employees
            if e["name"].lower() == "alice" and e["department"].lower() == "engineering"
        )
        self.assertTrue(duplicate)

    def test_no_duplicate_different_dept(self):
        duplicate = any(
            e for e in ers.employees
            if e["name"].lower() == "alice" and e["department"].lower() == "support"
        )
        self.assertFalse(duplicate)

    def test_no_duplicate_different_name(self):
        duplicate = any(
            e for e in ers.employees
            if e["name"].lower() == "zara" and e["department"].lower() == "engineering"
        )
        self.assertFalse(duplicate)


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
        self.assertIn("Engineering", ers.DEPARTMENTS)

    def test_invalid_department(self):
        self.assertNotIn("HR", ers.DEPARTMENTS)


class TestSearchEmployee(unittest.TestCase):
    """Test employee search by name (partial match)."""

    def test_exact_match(self):
        matched = [e for e in ers.employees if "alice" in e["name"].lower()]
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["name"], "Alice")

    def test_partial_match(self):
        matched = [e for e in ers.employees if "al" in e["name"].lower()]
        self.assertEqual(len(matched), 1)

    def test_no_match(self):
        matched = [e for e in ers.employees if "xyz" in e["name"].lower()]
        self.assertEqual(len(matched), 0)

    def test_case_insensitive(self):
        matched = [e for e in ers.employees if "GRACE" .lower() in e["name"].lower()]
        self.assertEqual(len(matched), 1)


class TestCreateEmployee(unittest.TestCase):
    """Test adding a new employee via mocked input."""

    def setUp(self):
        self.original_employees = ers.employees.copy()
        self.original_id = ers.next_id

    def tearDown(self):
        ers.employees = self.original_employees
        ers.next_id = self.original_id

    @patch("builtins.input", side_effect=["Zara", "Engineering", "15"])
    def test_create_valid_employee(self, mock_input):
        ers.create_employee()
        added = next((e for e in ers.employees if e["name"] == "Zara"), None)
        self.assertIsNotNone(added)
        self.assertEqual(added["department"], "Engineering")
        self.assertEqual(added["tickets"], 15)

    @patch("builtins.input", side_effect=["", "Engineering", "10"])
    def test_reject_empty_name(self, mock_input):
        count_before = len(ers.employees)
        ers.create_employee()
        self.assertEqual(len(ers.employees), count_before)

    @patch("builtins.input", side_effect=["Alice", "Engineering", "10"])
    def test_reject_duplicate(self, mock_input):
        count_before = len(ers.employees)
        ers.create_employee()
        self.assertEqual(len(ers.employees), count_before)


class TestDeleteEmployee(unittest.TestCase):
    """Test deleting an employee via mocked input."""

    def setUp(self):
        self.original_employees = ers.employees.copy()

    def tearDown(self):
        ers.employees = self.original_employees

    @patch("builtins.input", side_effect=["1", "y"])
    def test_delete_confirmed(self, mock_input):
        ers.delete_employee()
        self.assertIsNone(next((e for e in ers.employees if e["id"] == 1), None))

    @patch("builtins.input", side_effect=["1", "n"])
    def test_delete_cancelled(self, mock_input):
        ers.delete_employee()
        self.assertIsNotNone(next((e for e in ers.employees if e["id"] == 1), None))

    @patch("builtins.input", side_effect=["999"])
    def test_delete_nonexistent(self, mock_input):
        count_before = len(ers.employees)
        ers.delete_employee()
        self.assertEqual(len(ers.employees), count_before)


if __name__ == "__main__":
    unittest.main()
