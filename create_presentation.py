from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color scheme
WHITE_BG = RGBColor(0xFF, 0xFF, 0xFF)
ACCENT = RGBColor(0x1A, 0x56, 0xDB)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1E, 0x1E, 0x1E)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
GREEN = RGBColor(0x16, 0x7F, 0x3D)
PEACH = RGBColor(0xC0, 0x39, 0x2B)
MAUVE = RGBColor(0x6C, 0x3C, 0xB0)
YELLOW = RGBColor(0xB8, 0x86, 0x0B)
FONT_NAME = "Calibri"


def set_slide_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_text_box(slide, left, top, width, height, text, font_size=18,
                 color=BLACK, bold=False, alignment=PP_ALIGN.LEFT):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = FONT_NAME
    p.alignment = alignment
    return tf


def add_bullet_list(slide, left, top, width, height, items, font_size=16, color=DARK_GRAY):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = color
        p.font.name = FONT_NAME
        p.space_after = Pt(8)
        p.level = 0
    return tf


# ── Slide 1: Title ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(1), Inches(1.8), Inches(11), Inches(1.2),
             "Employee Records System", font_size=44, color=ACCENT, bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(3.2), Inches(11), Inches(0.8),
             "A Python CLI Application for Tracking Weekly Employee Metrics",
             font_size=22, color=DARK_GRAY, alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(4.5), Inches(11), Inches(0.6),
             "Belvah Shanyisa  •  April 2026",
             font_size=18, color=MAUVE, alignment=PP_ALIGN.CENTER)

# ── Slide 2: Problem Statement ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Problem Statement", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(4.5), [
    "• Teams need a simple way to track how many tickets each employee completes weekly",
    "• Manual tracking is error-prone and hard to visualize",
    "• Managers need quick views — by department or across the whole team",
    "• Metrics should be ranked from highest to lowest per department",
    "• Different colors needed to visually distinguish employees in charts",
    "• A lightweight CLI tool solves this without needing a full web app",
], font_size=20)

# ── Slide 3: Features ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Features", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5), [
    "• View all records ranked by tickets",
    "• Filter and view by department",
    "• Search employees by name (partial match)",
    "• Add new employees with validation",
    "• Update employee details by ID",
    "• Delete employees with confirmation",
], font_size=18)
add_bullet_list(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(5), [
    "• Terminal bar chart with Unicode symbols",
    "• Matplotlib graphical chart with color coding",
    "• Dynamic color palettes — unique shade per employee",
    "• Duplicate prevention (same name + dept)",
    "• Input validation (alphanumeric names, non-negative tickets)",
], font_size=18)

# ── Slide 4: Bar Chart Visualization ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Bar Chart Visualization", font_size=36, color=ACCENT, bold=True)
slide.shapes.add_picture(
    "/Users/shanyisa/Desktop/Screenshot 2026-04-20 at 00.23.59.png",
    Inches(1.5), Inches(1.6), Inches(10.3), Inches(5.5))

# ── Slide 5: Tech Stack ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Tech Stack", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(4.5), [
    "• Python 3 — core language",
    "• matplotlib — graphical bar charts with color-coded department palettes",
    "• colorsys — built-in HSL-to-RGB color conversion for dynamic shading",
    "• In-memory storage — list of dictionaries (data resets on exit)",
], font_size=20)

# ── Slide 5: Code Structure ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Code Structure", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5), [
    "Data Layer",
    "  • employees list (8 seed records)",
    "  • DEPARTMENTS constant",
    "  • get_next_id() for auto-incrementing IDs",
    "",
    "Visualization Layer",
    "  • show_terminal_chart() — Unicode bar chart",
    "  • show_matplotlib_chart() — graphical chart",
    "  • generate_palette() — dynamic color shading",
], font_size=16, color=DARK_GRAY)
add_bullet_list(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(5), [
    "CRUD Functions",
    "  • create_employee() — with full validation",
    "  • update_employee() — partial updates supported",
    "  • delete_employee() — with confirmation",
    "",
    "  • search_employee() — partial name match",
    "",
    "Display & Menu",
    "  • display_records() — ranked table output",
    "  • view_all() / view_by_department()",
    "  • main() — while loop menu (options 1-7)",
], font_size=16, color=DARK_GRAY)

# ── Slide 6: Key Concepts Used ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Key Python Concepts Used", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5), [
    "• Lists and dictionaries",
    "• Functions with parameters and return values",
    "• Global variables and scope",
    "• While loops and conditionals",
    "• String formatting (f-strings)",
], font_size=20)
add_bullet_list(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(5), [
    "• Input validation and error handling (try/except)",
    "• List comprehensions and filtering",
    "• Sorting with lambda functions",
    "• Importing and using external libraries",
    "• Constants and configuration patterns",
], font_size=20)

# ── Slide 7: Validation Rules ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Validation Rules", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(4.5), [
    "• Username must be alphanumeric only (no spaces or special characters)",
    "• Username cannot be empty",
    "• Department must match one of the 5 predefined departments",
    "• No duplicate employee with same name + department (case-insensitive)",
    "• Ticket count must be a non-negative integer",
    "• Invalid input is caught with try/except — program never crashes",
], font_size=20)

# ── Slide 8: Demo – Main Menu ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Demo — Main Menu", font_size=36, color=ACCENT, bold=True)
slide.shapes.add_picture(
    "/Users/shanyisa/Desktop/Screenshot 2026-04-20 at 00.23.23.png",
    Inches(1.5), Inches(1.6), Inches(10.3), Inches(5.5))

# ── Slide 9: Demo – Search by Name ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Demo — Search by Name", font_size=36, color=ACCENT, bold=True)
slide.shapes.add_picture(
    "/Users/shanyisa/Desktop/Screenshot 2026-04-20 at 00.25.17.png",
    Inches(1.5), Inches(1.6), Inches(10.3), Inches(5.5))

# ── Slide 10: Demo – Bar Chart ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Demo — Bar Chart Visualization", font_size=36, color=ACCENT, bold=True)
slide.shapes.add_picture(
    "/Users/shanyisa/Desktop/Screenshot 2026-04-20 at 00.25.41.png",
    Inches(1.5), Inches(1.6), Inches(10.3), Inches(5.5))

# ── Slide 12: Challenges & Lessons Learned ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Challenges & Lessons Learned", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5), [
    "Challenges",
    "  • Generating unique color shades per employee",
    "  • Aligning terminal bar chart with Unicode characters",
    "  • Handling edge cases in user input",
    "  • Keeping code organized as features grew",
], font_size=18, color=PEACH)
add_bullet_list(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(5), [
    "Lessons Learned",
    "  • Breaking code into small focused functions",
    "  • Input validation prevents crashes",
    "  • f-strings make formatting clean and readable",
    "  • matplotlib is powerful for quick visualizations",
    "  • Unit testing catches bugs early",
], font_size=18, color=GREEN)

# ── Slide 12: Future Improvements ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Future Improvements", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(4.5), [
    "• SQLite database for persistent storage",
    "• Export records to CSV, TXT, PDF, and Excel",
    "• Support custom departments via configuration",
], font_size=20)

# ── Slide 13: Unit Testing ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Unit Testing", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(5.5), Inches(5), [
    "32 automated tests using unittest",
    "",
    "• ID generation — auto-incrementing",
    "• Color palettes — valid hex, unique shades",
    "• Department filtering — by name, case-insensitive",
    "• Sorting — descending order by tickets",
    "• Duplicate detection — same name+dept blocked",
], font_size=18)
add_bullet_list(slide, Inches(6.5), Inches(1.8), Inches(6), Inches(5), [
    "Run tests:",
    "  python -m unittest test_employees -v",
    "",
    "• Input validation — alphanumeric, empty, departments",
    "• Search — exact, partial, case-insensitive",
    "• Create employee — valid add, reject duplicates",
    "• Delete employee — confirm, cancel, nonexistent",
    "",
    "All 32 tests pass in 0.003 seconds",
], font_size=18)

# ── Slide 14: Conclusion ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(0.8), Inches(0.5), Inches(11), Inches(0.8),
             "Conclusion", font_size=36, color=ACCENT, bold=True)
add_bullet_list(slide, Inches(0.8), Inches(1.8), Inches(11), Inches(4.5), [
    "• Built a fully functional CLI app to track employee weekly ticket completions",
    "• Implemented full CRUD operations with robust input validation",
    "• Created dual visualizations — terminal chart and matplotlib graphical chart",
    "• Each employee gets a unique color shade within their department",
    "• Added search functionality and 32 passing unit tests",
    "• The project demonstrates core Python skills: functions, data structures, loops, error handling, and libraries",
], font_size=20)

# ── Slide 15: Q&A ──
slide = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_bg(slide, WHITE_BG)
add_text_box(slide, Inches(1), Inches(2), Inches(11), Inches(1),
             "Questions?", font_size=44, color=ACCENT, bold=True,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(3.5), Inches(11), Inches(0.6),
             "GitHub: github.com/Belvah", font_size=20, color=DARK_GRAY,
             alignment=PP_ALIGN.CENTER)
add_text_box(slide, Inches(1), Inches(4.3), Inches(11), Inches(0.6),
             "Belvah Shanyisa  •  misshuey3@gmail.com", font_size=18,
             color=MAUVE, alignment=PP_ALIGN.CENTER)

# Save
output_path = "/Users/shanyisa/Desktop/python_foundations/python_intro/employee_weekly/Employee_Records_System_Presentation.pptx"
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
