"""Visualization module for the Employee Records System.

Provides terminal-based and matplotlib-based bar chart displays
for employee ticket data, with department-specific color palettes.
"""

import colorsys  # Built-in module for converting HSL colors to RGB

import matplotlib.pyplot as plt           # Creates the graphical bar chart window
import matplotlib.patches as mpatches     # Used to build the color legend on the chart

from database import DEPARTMENTS  # Shared list of valid departments

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

# Base HSL colors per department for matplotlib chart
DEPT_BASE_COLORS = {
    "Engineering": (0.58, 0.85, 0.70),
    "Support":     (0.33, 0.85, 0.70),
    "Compliance":  (0.75, 0.65, 0.70),
    "Security":    (0.00, 0.80, 0.70),
    "Marketing":   (0.08, 0.85, 0.70),
}


def generate_palette(dept, count):
    """Create shade variations for employees in the same department.

    Uses the department's base HSL color and generates `count` distinct
    shades by varying lightness and saturation.

    Args:
        dept: Department name (used to look up base color).
        count: Number of color shades to generate.

    Returns:
        A list of hex color strings (e.g. ['#4a8bc2', '#6faed4']).
    """
    # Fall back to gray if department is unknown
    base_h, base_s, base_l = DEPT_BASE_COLORS.get(dept, (0.0, 0.0, 0.60))
    if count == 1:  # Only one employee in the dept — use the base color directly
        r, g, b = colorsys.hls_to_rgb(base_h, base_l, base_s)
        return [f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"]
    colors = []
    for i in range(count):
        # Spread lightness across a range so each employee gets a distinct shade
        lightness = base_l - 0.20 + (0.40 * i / (count - 1))
        lightness = max(0.25, min(0.90, lightness))  # Clamp to avoid pure black or white
        saturation = base_s - (0.15 * i / (count - 1))
        saturation = max(0.30, min(1.0, saturation))
        r, g, b = colorsys.hls_to_rgb(base_h, lightness, saturation)
        colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
    return colors


def get_employee_color(emp, all_employees):
    """Assign a unique shade to an employee based on department rank.

    Employees within the same department are sorted by tickets (descending)
    and each gets a different shade from the department's palette.

    Args:
        emp: Dict with keys id, name, department, tickets.
        all_employees: List of all employee dicts (used to rank within dept).

    Returns:
        A hex color string for this employee.
    """
    dept = emp["department"]
    # Filter to same-department employees and rank by tickets (highest first)
    dept_employees = sorted(
        [e for e in all_employees if e["department"] == dept],
        key=lambda e: e["tickets"], reverse=True,
    )
    palette = generate_palette(dept, len(dept_employees))  # One shade per dept employee
    idx = next((i for i, e in enumerate(dept_employees) if e["id"] == emp["id"]), 0)  # Find this employee's rank
    return palette[idx]


def show_terminal_chart(records, title="Employee Weekly Metrics"):
    """Print a horizontal bar chart in the terminal using Unicode symbols.

    Each bar's length is proportional to the employee's ticket count
    relative to the maximum in the dataset.

    Args:
        records: List of employee dicts to chart.
        title: Title string displayed above the chart.
    """
    if not records:
        print("\nNo records to chart.")
        return
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True)
    max_tickets = max(e["tickets"] for e in sorted_records)
    max_name = max(len(e["name"]) for e in sorted_records)

    print(f"\n  {title}")
    print(f"  {'=' * (max_name + BAR_WIDTH + 12)}")

    for emp in sorted_records:
        # Scale bar length proportionally: highest tickets = full bar width
        bar_len = int((emp["tickets"] / max_tickets) * BAR_WIDTH) if max_tickets > 0 else 0
        symbol = DEPT_SYMBOLS.get(emp["department"], "█")  # Each dept has its own Unicode character
        bar = symbol * bar_len  # Repeat the symbol to create the bar
        print(f"  {emp['name']:<{max_name}}  |{bar:<{BAR_WIDTH}}| {emp['tickets']}")

    print()
    legend = "  Legend: " + "  ".join(
        f"{sym} {dept}" for dept, sym in DEPT_SYMBOLS.items()
        if any(e["department"] == dept for e in sorted_records)
    )
    print(legend)
    print()


def show_matplotlib_chart(records, title="Employee Weekly Metrics"):
    """Open a graphical horizontal bar chart using matplotlib.

    Employees are colored by department with unique shades per person.
    A legend identifies each department.

    Args:
        records: List of employee dicts to chart.
        title: Title string displayed on the chart.
    """
    if not records:
        return
    sorted_records = sorted(records, key=lambda e: e["tickets"], reverse=True)
    names = [e["name"] for e in sorted_records]
    tickets = [e["tickets"] for e in sorted_records]
    colors = [get_employee_color(e, records) for e in sorted_records]

    # Create figure — height scales with number of employees so bars don't get squished
    fig, ax = plt.subplots(figsize=(10, max(4, len(names) * 0.6)))
    # [::-1] reverses the list so highest tickets appear at the top of the chart
    bars = ax.barh(names[::-1], tickets[::-1], color=colors[::-1], edgecolor="#333333", linewidth=0.5)

    # Add ticket count label at the end of each bar for readability
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


def show_bar_chart(records, title="Employee Weekly Metrics"):
    """Show terminal chart, then optionally open a graphical matplotlib chart.

    Displays the terminal chart first, then prompts the user whether
    to open the graphical version.

    Args:
        records: List of employee dicts to chart.
        title: Title string for both charts.
    """
    show_terminal_chart(records, title)
    open_chart = input("Open graphical chart? (y/n): ").strip().lower()
    if open_chart == "y":
        show_matplotlib_chart(records, title)
