# 🎓 Student Result & Grade Management System

A simple, robust, and beginner-friendly menu-driven Command Line Interface (CLI) application built with Python. Designed for an internship project, this application manages student records, validates marks across 5 core academic subjects, calculates percentage, letter grades, and pass/fail statuses automatically, and generates comprehensive class performance reports.

Built strictly using **Python fundamentals** and the **Python standard library** (zero external dependencies).

---

## 📋 Table of Contents
- [Project Overview](#-project-overview)
- [Project Structure](#-project-structure)
- [Features](#-features)
- [Grading Scale & Passing Criteria](#-grading-scale--passing-criteria)
- [How to Run](#-how-to-run)
- [Sample Menu & Outputs](#-sample-menu--outputs)
  - [1. Main Menu](#1-main-menu)
  - [2. View All Students](#2-view-all-students)
  - [3. Add Student (with Validation)](#3-add-student-with-validation)
  - [4. Search Student](#4-search-student)
  - [5. Performance Summary Report](#5-performance-summary-report)
- [What I Learned](#-what-i-learned)
- [Screenshots Guide](#-screenshots-guide)

---

## 📌 Project Overview

This project simulates a real-world student grading and academic performance management system. It emphasizes clean code structure, modular design, readable variable names, docstrings for every function, and bulletproof user input handling so the application never crashes.

### Core Subjects Covered (5 Core Subjects)
1. **Maths**
2. **Science**
3. **English**
4. **Computer Science**
5. **Social Studies**

---

## 📁 Project Structure

```text
student-management-system/
├── main.py               # menu-driven CLI entry point
├── student_manager.py    # add, update, delete, view, search students
├── grade_calculator.py   # grade calculation module
├── performance.py        # performance summary and reports
├── data/students.json    # persistent storage
├── README.md             # project documentation
└── screenshots/          # placeholder folder for sample output
```

### Module Responsibilities
- **`main.py`**: CLI entry point with an interactive menu loop, routing commands, and handling graceful exit and exceptions (`KeyboardInterrupt`, `EOFError`).
- **`student_manager.py`**: Handles student CRUD operations (Add, Update, Delete with confirmation, View in a formatted table, Search by roll or name) and persistent JSON read/write operations.
- **`grade_calculator.py`**: Validates numeric marks (0-100), computes total marks, percentage, assigns letter grades, and determines pass/fail criteria.
- **`performance.py`**: Calculates and presents class analytics, highest and lowest scorers, grade distribution chart, pass percentage, and subject-wise averages.
- **`data/students.json`**: JSON file holding student records as a list of dictionaries with 5 pre-loaded sample students.

---

## ✨ Features

1. **Add Student**:
   - Collects unique roll number, validated student name, and marks for 5 core subjects.
   - Computes total marks, percentage, grade, and pass/fail status automatically.
   - Immediately persists new records to `data/students.json`.
2. **Update Student**:
   - Find existing student by roll number (case-insensitive).
   - Allows updating the student's name, all subject marks, or an individual subject mark.
   - Recalculates all results automatically.
3. **Delete Student**:
   - Deletes student record by roll number.
   - Includes safety confirmation prompt (`y/n`) before permanent removal.
4. **View All Students**:
   - Displays all records in a cleanly formatted ASCII table with properly aligned columns for Roll Number, Name, all 5 subjects, Total, Percentage, Grade, and Status.
5. **Search Student**:
   - Search by roll number or student name.
   - Supports case-insensitive and partial name matching.
   - Displays a detailed student result card with individual subject breakdown.
6. **Grade Calculation**:
   - Automatic calculation of total (out of 500), percentage, and letter grade.
   - Enforces pass/fail criteria.
7. **Performance Summary**:
   - Class average percentage.
   - Top performer (highest score) and lowest performer details.
   - Grade distribution breakdown with visual text-based bar chart.
   - Overall pass percentage and counts.
   - Subject-wise average marks.
8. **Input Validation & Error Handling**:
   - Marks must be numeric and between 0 and 100.
   - Roll number cannot be empty and must be unique.
   - Name must contain only alphabetic characters and spaces.
   - Menu choices and unexpected inputs are handled with `try/except` without crashing.

---

## 📊 Grading Scale & Passing Criteria

The grading system is implemented in `grade_calculator.py` according to the following academic standard:

| Percentage Range | Grade | Description | Academic Status |
|:---:|:---:|:---:|:---:|
| **90% – 100%** | **A+** | Outstanding | Pass |
| **80% – 89.9%** | **A** | Excellent | Pass |
| **70% – 79.9%** | **B** | Very Good | Pass |
| **60% – 69.9%** | **C** | Good | Pass |
| **50% – 59.9%** | **D** | Satisfactory | Pass |
| **Below 50%** | **F** | Fail | Fail |

### Passing Rules:
- **Individual Subject Passing Mark**: A student must score **at least 35 marks** in every subject. Scoring below 35 in any subject results in an automatic **Fail** status.
- **Overall Percentage**: A student must achieve an aggregate percentage of **at least 50%** to pass.

---

## 🚀 How to Run

### Prerequisites
- Python 3.8 or higher installed on your computer.
- Check version:
  ```bash
  python --version
  ```

### Steps to Run
1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd student-management-system
   ```
3. Run the application:
   ```bash
   python main.py
   ```

*(No additional packages or third-party libraries required!)*

---

## 💻 Sample Menu & Outputs

### 1. Main Menu
```text
*******************************************************
 Welcome to Student Result & Grade Management System
*******************************************************
Loaded 5 student record(s) from 'data/students.json'.

=======================================================
      STUDENT RESULT & GRADE MANAGEMENT SYSTEM
=======================================================
  1. Add Student
  2. Update Student
  3. Delete Student
  4. View All Students
  5. Search Student
  6. Performance Summary
  7. Exit
=======================================================
Enter your choice (1-7, or 'q' to exit):
```

---

### 2. View All Students
Displays all 5 pre-loaded sample records in a neatly aligned table:
```text
================================================================================================
                               ALL STUDENT RECORDS
================================================================================================
+--------+------------------+-------+-------+-------+-------+-------+--------+--------+-------+--------+
| Roll   | Name             | Math  | Sci   | Eng   | CS    | SS    | Total  | Pct %  | Grade | Status |
+--------+------------------+-------+-------+-------+-------+-------+--------+--------+-------+--------+
| 101    | Aarav Sharma     |  95.0 |  92.0 |  88.0 |  96.0 |  90.0 |  461.0 |  92.2% |  A+   |  Pass  |
| 102    | Diya Patel       |  85.0 |  82.0 |  88.0 |  84.0 |  86.0 |  425.0 |  85.0% |   A   |  Pass  |
| 103    | Rohan Verma      |  75.0 |  72.0 |  70.0 |  78.0 |  75.0 |  370.0 |  74.0% |   B   |  Pass  |
| 104    | Sneha Reddy      |  62.0 |  65.0 |  58.0 |  68.0 |  62.0 |  315.0 |  63.0% |   C   |  Pass  |
| 105    | Kabir Khan       |  45.0 |  32.0 |  52.0 |  48.0 |  50.0 |  227.0 |  45.4% |   F   |  Fail  |
+--------+------------------+-------+-------+-------+-------+-------+--------+--------+-------+--------+
  Total Students: 5
================================================================================================
```

---

### 3. Add Student (with Validation)
Shows input validation rejecting duplicate roll numbers, non-alphabetic names, and out-of-range marks:
```text
=======================================================
                 ADD NEW STUDENT
=======================================================
  Enter Roll Number (e.g. 106): 101
    [Error] Roll number '101' already exists! Each student must have a unique roll number.
  Enter Roll Number (e.g. 106): 106
  Enter Student Full Name: John123
    [Error] Name must contain only letters and spaces (no numbers or symbols).
  Enter Student Full Name: Ishaan Verma

  Enter marks for each of the 5 subjects (0 to 100):
  Enter marks for Maths (0-100): 105
    [Error] Marks must be between 0 and 100. You entered: 105.0
  Enter marks for Maths (0-100): 88
  Enter marks for Science (0-100): 85
  Enter marks for English (0-100): 90
  Enter marks for Computer Science (0-100): 92
  Enter marks for Social Studies (0-100): 86

-------------------------------------------------------
  [Success] Student 'Ishaan Verma' (Roll No: 106) added successfully!
  Total Marks : 441.0 / 500
  Percentage  : 88.2%
  Grade       : A  |  Status: Pass
-------------------------------------------------------
```

---

### 4. Search Student
Search by Name with case-insensitive partial match:
```text
=======================================================
                 SEARCH STUDENTS
=======================================================
  Search Criteria:
  1. Search by Roll Number
  2. Search by Name (partial match allowed)
  3. Cancel and Return to Main Menu
  Enter choice (1-3): 2
  Enter Student Name to search: Aarav

  Found 1 matching student record(s):

  ------------------------------------------------
    Roll Number : 101
    Name        : Aarav Sharma
    Total Marks : 461.0 / 500
    Percentage  : 92.2%
    Grade       : A+
    Status      : Pass
    Subject Breakdown:
      - Maths             :  95.0 / 100 (Pass)
      - Science           :  92.0 / 100 (Pass)
      - English           :  88.0 / 100 (Pass)
      - Computer Science  :  96.0 / 100 (Pass)
      - Social Studies    :  90.0 / 100 (Pass)
  ------------------------------------------------
```

---

### 5. Performance Summary Report
Generates class-wide analytics and visual grade distribution:
```text
====================================================================
                 CLASS PERFORMANCE SUMMARY REPORT
====================================================================
  Total Students Enrolled : 5
  Class Average Percentage: 71.92%
  Overall Pass Percentage : 80.0% (4 Passed, 1 Failed)
--------------------------------------------------------------------
  TOP PERFORMER (Highest Scorer):
    * Name       : Aarav Sharma
    * Roll Number: 101
    * Score      : 461.0/500 (92.2%) - Grade A+

  LOWEST PERFORMER:
    - Name       : Kabir Khan
    - Roll Number: 105
    - Score      : 227.0/500 (45.4%) - Grade F [Fail]
--------------------------------------------------------------------
  GRADE DISTRIBUTION:
    A+ (90 - 100%   ) : [####                ]  1 student(s) ( 20.0%)
    A  (80 - 89.9%  ) : [####                ]  1 student(s) ( 20.0%)
    B  (70 - 79.9%  ) : [####                ]  1 student(s) ( 20.0%)
    C  (60 - 69.9%  ) : [####                ]  1 student(s) ( 20.0%)
    D  (50 - 59.9%  ) : [                    ]  0 student(s) (  0.0%)
    F  (< 50% (Fail)) : [####                ]  1 student(s) ( 20.0%)
--------------------------------------------------------------------
  SUBJECT-WISE AVERAGE MARKS (Out of 100):
    Subject              |   Class Average
    ---------------------+----------------
    Maths                |         72.40 
    Science              |         68.60 
    English              |         71.20 
    Computer Science     |         74.80 
    Social Studies       |         72.60 
====================================================================
```

---

## 💡 What I Learned

During the development of this project, I strengthened my understanding of key software engineering and Python fundamentals:

1. **Modular Programming & Separation of Concerns**:
   - Structured the project into dedicated modules (`main.py`, `student_manager.py`, `grade_calculator.py`, `performance.py`), making code maintainable, reusable, and easy to debug.
2. **Data Modeling with Lists and Dictionaries**:
   - Stored records as a list of dictionaries, representing student entities with nested dictionaries for individual subject scores.
3. **Data Persistence with JSON**:
   - Implemented load and save routines using Python's built-in `json` module, ensuring student records persist across program executions.
4. **Defensive Programming & Input Validation**:
   - Used loop-based re-prompting and `try/except` exception handling to validate types (e.g., preventing string input where a float mark is expected), ranges (0-100), string formatting (letters and spaces only), and uniqueness of roll numbers.
5. **Data Aggregation & Statistical Algorithms**:
   - Computed class metrics such as average percentage, subject-wise averages, identifying maximum and minimum performers using Python's `max()` and `min()` with lambda key functions, and tallying grade distributions.
6. **Command Line Interface (CLI) Formatting**:
   - Formatted tabular data using Python string formatting (`:<`, `:>`, `:^`) to create neat ASCII tables and visual bar charts directly in the terminal without external packages.

---

## 📷 Screenshots Guide

When taking screenshots for project submissions or GitHub portfolios, capture:
1. **`01_main_menu.png`**: The application banner and main menu.
2. **`02_view_all_students.png`**: The formatted ASCII table showing all 5 sample records.
3. **`03_add_student_validation.png`**: Entering student data showing error prompts for invalid input and successful creation.
4. **`04_search_student.png`**: Searching for a student and viewing their result card.
5. **`05_performance_summary.png`**: The class performance summary report with grade distribution and subject averages.

Save your screenshots in the `screenshots/` directory.
