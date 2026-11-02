"""
student_manager.py - Core student management operations module.

This module provides functions to:
1. add_student()        - Register a new student with unique roll number and validated marks.
2. update_student()     - Update existing student's name or subject marks.
3. delete_student()     - Delete a student record with confirmation.
4. view_all_students()  - Display all students in a neatly formatted table.
5. search_student()     - Search students by roll number or name (case-insensitive, partial matching).
6. load_students()      - Load student records from JSON storage.
7. save_students()      - Persist student records to JSON storage.
"""

import json
import os
from grade_calculator import (
    SUBJECTS,
    validate_mark_input,
    calculate_student_result,
)


def load_students(filepath: str) -> list:
    """
    Load student records from the specified JSON file.

    If the file does not exist, an empty list is returned and the directory
    is created so future saves succeed seamlessly.

    Args:
        filepath (str): Path to the students JSON file.

    Returns:
        list: List of student dictionaries.
    """
    if not os.path.exists(filepath):
        # Ensure parent directory exists
        dir_name = os.path.dirname(filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)

            if not isinstance(data, list):
                print("  [Warning] Data format in storage was not a list. Initializing empty list.")
                return []

            # Ensure calculated fields are consistent
            for student in data:
                if "marks" in student and isinstance(student["marks"], dict):
                    total, percentage, grade, status = calculate_student_result(student["marks"])
                    student["total"] = total
                    student["percentage"] = percentage
                    student["grade"] = grade
                    student["status"] = status

            return data

    except (json.JSONDecodeError, IOError) as e:
        print(f"  [Warning] Could not parse JSON from '{filepath}': {e}. Using empty records.")
        return []


def save_students(students: list, filepath: str) -> bool:
    """
    Save the list of student dictionaries to a JSON file.

    Args:
        students (list): List of student dictionaries.
        filepath (str): Target JSON file path.

    Returns:
        bool: True if saving succeeded, False otherwise.
    """
    try:
        dir_name = os.path.dirname(filepath)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(students, f, indent=4)
        return True
    except IOError as e:
        print(f"  [Error] Failed to save data to '{filepath}': {e}")
        return False


def is_valid_name(name: str) -> bool:
    """
    Validate that the name contains only alphabetic characters and spaces.

    Args:
        name (str): The name string to check.

    Returns:
        bool: True if valid and non-empty, False otherwise.
    """
    cleaned = name.strip()
    if not cleaned:
        return False
    # Check that all characters are letters or spaces
    return all(c.isalpha() or c.isspace() for c in cleaned)


def prompt_valid_name(prompt_text: str = "Enter Student Name: ") -> str:
    """
    Prompt the user repeatedly until a valid alphabetic name is provided.

    Args:
        prompt_text (str): Input prompt message.

    Returns:
        str: Validated student name with extra whitespace stripped.
    """
    while True:
        name = input(prompt_text).strip()
        if not name:
            print("    [Error] Name cannot be empty. Please enter a valid name.")
            continue
        if not is_valid_name(name):
            print("    [Error] Name must contain only letters and spaces (no numbers or symbols).")
            continue
        # Format name nicely with title case
        return " ".join(name.split()).title()


def prompt_unique_roll(students: list, prompt_text: str = "Enter Roll Number: ") -> str:
    """
    Prompt the user repeatedly until a non-empty, unique roll number is entered.

    Args:
        students (list): Existing list of student dictionaries.
        prompt_text (str): Input prompt message.

    Returns:
        str: Unique roll number string.
    """
    while True:
        roll_number = input(prompt_text).strip()
        if not roll_number:
            print("    [Error] Roll number cannot be empty.")
            continue

        # Check for case-insensitive duplicate
        is_duplicate = any(s["roll_number"].lower() == roll_number.lower() for s in students)
        if is_duplicate:
            print(f"    [Error] Roll number '{roll_number}' already exists! Each student must have a unique roll number.")
            continue

        return roll_number


def add_student(students: list, filepath: str) -> None:
    """
    Add a new student with roll number, name, and marks for 5 subjects.
    Automatically computes total, percentage, grade, and pass/fail status,
    then saves the record to the JSON storage.

    Args:
        students (list): List of student records.
        filepath (str): Filepath to persist the new record.
    """
    print("\n" + "=" * 55)
    print("                 ADD NEW STUDENT")
    print("=" * 55)

    # 1. Roll Number
    roll_number = prompt_unique_roll(students, "  Enter Roll Number (e.g. 106): ")

    # 2. Student Name
    name = prompt_valid_name("  Enter Student Full Name: ")

    # 3. Enter Marks for all 5 subjects
    print("\n  Enter marks for each of the 5 subjects (0 to 100):")
    marks = {}
    for subject in SUBJECTS:
        mark = validate_mark_input(subject)
        marks[subject] = mark

    # 4. Calculate Results
    total, percentage, grade, status = calculate_student_result(marks)

    # 5. Construct Record and Append
    student = {
        "roll_number": roll_number,
        "name": name,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "grade": grade,
        "status": status
    }

    students.append(student)
    save_students(students, filepath)

    # 6. Display Success Summary
    print("\n" + "-" * 55)
    print(f"  [Success] Student '{name}' (Roll No: {roll_number}) added successfully!")
    print(f"  Total Marks : {total} / 500")
    print(f"  Percentage  : {percentage}%")
    print(f"  Grade       : {grade}  |  Status: {status}")
    print("-" * 55)


def update_student(students: list, filepath: str) -> None:
    """
    Update the name or subject marks of an existing student by roll number.
    Recalculates results automatically after updates and saves to JSON.

    Args:
        students (list): List of student records.
        filepath (str): Filepath to persist updates.
    """
    print("\n" + "=" * 55)
    print("                 UPDATE STUDENT")
    print("=" * 55)

    if not students:
        print("  [Info] No student records available to update.")
        return

    roll_number = input("  Enter Roll Number of the student to update: ").strip()

    # Find student (case-insensitive)
    student = next((s for s in students if s["roll_number"].lower() == roll_number.lower()), None)

    if not student:
        print(f"  [Error] No student found with Roll Number '{roll_number}'.")
        return

    print(f"\n  Current Student Details:")
    print(f"  Roll No   : {student['roll_number']}")
    print(f"  Name      : {student['name']}")
    print(f"  Marks     : {student['marks']}")
    print(f"  Percentage: {student['percentage']}%  |  Grade: {student['grade']}  |  Status: {student['status']}")

    while True:
        print("\n  What would you like to update?")
        print("  1. Update Name")
        print("  2. Update All Subject Marks")
        print("  3. Update a Specific Subject Mark")
        print("  4. Finish and Return to Main Menu")

        choice = input("  Enter your choice (1-4): ").strip()

        if choice == "1":
            new_name = prompt_valid_name(f"  Enter new name (current: '{student['name']}'): ")
            student["name"] = new_name
            save_students(students, filepath)
            print(f"  [Success] Student name updated to '{new_name}'.")

        elif choice == "2":
            print("\n  Enter new marks for all 5 subjects (0 to 100):")
            new_marks = {}
            for subject in SUBJECTS:
                new_marks[subject] = validate_mark_input(subject)

            student["marks"] = new_marks
            total, percentage, grade, status = calculate_student_result(new_marks)
            student["total"] = total
            student["percentage"] = percentage
            student["grade"] = grade
            student["status"] = status
            save_students(students, filepath)
            print(f"  [Success] All marks updated! New Total: {total}, Percentage: {percentage}%, Grade: {grade}, Status: {status}")

        elif choice == "3":
            print("\n  Select subject to update:")
            for idx, subject in enumerate(SUBJECTS, 1):
                cur_mark = student["marks"].get(subject, 0.0)
                print(f"    {idx}. {subject:<16} (Current: {cur_mark})")

            subj_choice = input(f"  Select subject (1-{len(SUBJECTS)}): ").strip()
            try:
                subj_idx = int(subj_choice) - 1
                if 0 <= subj_idx < len(SUBJECTS):
                    target_subject = SUBJECTS[subj_idx]
                    new_mark = validate_mark_input(target_subject)
                    student["marks"][target_subject] = new_mark

                    total, percentage, grade, status = calculate_student_result(student["marks"])
                    student["total"] = total
                    student["percentage"] = percentage
                    student["grade"] = grade
                    student["status"] = status
                    save_students(students, filepath)
                    print(f"  [Success] Marks for '{target_subject}' updated to {new_mark}!")
                    print(f"  New Percentage: {percentage}%, Grade: {grade}, Status: {status}")
                else:
                    print(f"  [Error] Invalid subject number. Must be between 1 and {len(SUBJECTS)}.")
            except ValueError:
                print("  [Error] Invalid input. Please enter a valid number.")

        elif choice == "4":
            print(f"  [Info] Completed updating record for '{student['name']}'.")
            break

        else:
            print("  [Error] Invalid choice. Please enter 1, 2, 3, or 4.")


def delete_student(students: list, filepath: str) -> None:
    """
    Delete a student record by roll number after user confirmation.

    Args:
        students (list): List of student records.
        filepath (str): Filepath to persist deletion.
    """
    print("\n" + "=" * 55)
    print("                 DELETE STUDENT")
    print("=" * 55)

    if not students:
        print("  [Info] No student records available to delete.")
        return

    roll_number = input("  Enter Roll Number of the student to delete: ").strip()

    # Find student
    student_index = None
    for idx, s in enumerate(students):
        if s["roll_number"].lower() == roll_number.lower():
            student_index = idx
            break

    if student_index is None:
        print(f"  [Error] Student with Roll Number '{roll_number}' was not found.")
        return

    student = students[student_index]
    confirm = input(f"  Are you sure you want to delete '{student['name']}' (Roll No: {student['roll_number']})? (y/n): ").strip().lower()

    if confirm in ("y", "yes"):
        deleted_student = students.pop(student_index)
        save_students(students, filepath)
        print(f"  [Success] Student '{deleted_student['name']}' (Roll No: {deleted_student['roll_number']}) has been deleted.")
    else:
        print("  [Info] Deletion cancelled. Student record preserved.")


def view_all_students(students: list) -> None:
    """
    Display all student records in a neatly formatted table.

    Args:
        students (list): List of student records.
    """
    print("\n" + "=" * 96)
    print("                               ALL STUDENT RECORDS")
    print("=" * 96)

    if not students:
        print("  [Info] No student records found. Add students first.")
        print("=" * 96)
        return

    # Table Header and Formatter
    divider = "+" + "-" * 8 + "+" + "-" * 18 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 7 + "+" + "-" * 8 + "+" + "-" * 8 + "+" + "-" * 7 + "+" + "-" * 8 + "+"
    header  = f"| {'Roll':<6} | {'Name':<16} | {'Math':<5} | {'Sci':<5} | {'Eng':<5} | {'CS':<5} | {'SS':<5} | {'Total':<6} | {'Pct %':<6} | {'Grade':<5} | {'Status':<6} |"

    print(divider)
    print(header)
    print(divider)

    for s in students:
        marks = s.get("marks", {})
        m_math = marks.get("Maths", 0.0)
        m_sci  = marks.get("Science", 0.0)
        m_eng  = marks.get("English", 0.0)
        m_cs   = marks.get("Computer Science", 0.0)
        m_ss   = marks.get("Social Studies", 0.0)

        # Truncate long names cleanly if needed
        name_display = s["name"]
        if len(name_display) > 16:
            name_display = name_display[:13] + "..."

        row = (
            f"| {s['roll_number']:<6} "
            f"| {name_display:<16} "
            f"| {m_math:>5.1f} "
            f"| {m_sci:>5.1f} "
            f"| {m_eng:>5.1f} "
            f"| {m_cs:>5.1f} "
            f"| {m_ss:>5.1f} "
            f"| {s['total']:>6.1f} "
            f"| {s['percentage']:>5.1f}% "
            f"| {s['grade']:^5} "
            f"| {s['status']:^6} |"
        )
        print(row)

    print(divider)
    print(f"  Total Students: {len(students)}")
    print("=" * 96)


def search_student(students: list) -> None:
    """
    Search for students by roll number or name (case-insensitive, partial match allowed).
    Displays detailed result cards for all matching students.

    Args:
        students (list): List of student records.
    """
    print("\n" + "=" * 55)
    print("                 SEARCH STUDENTS")
    print("=" * 55)

    if not students:
        print("  [Info] No student records available to search.")
        return

    print("  Search Criteria:")
    print("  1. Search by Roll Number")
    print("  2. Search by Name (partial match allowed)")
    print("  3. Cancel and Return to Main Menu")

    choice = input("  Enter choice (1-3): ").strip()

    if choice == "1":
        query = input("  Enter Roll Number to search: ").strip()
        if not query:
            print("  [Error] Search term cannot be empty.")
            return
        matches = [s for s in students if query.lower() in s["roll_number"].lower()]

    elif choice == "2":
        query = input("  Enter Student Name to search: ").strip()
        if not query:
            print("  [Error] Search term cannot be empty.")
            return
        matches = [s for s in students if query.lower() in s["name"].lower()]

    elif choice == "3":
        print("  [Info] Search cancelled.")
        return

    else:
        print("  [Error] Invalid choice. Returning to main menu.")
        return

    if not matches:
        print(f"\n  [Info] No students found matching '{query}'.")
        return

    print(f"\n  Found {len(matches)} matching student record(s):")
    for s in matches:
        print("\n  " + "-" * 48)
        print(f"    Roll Number : {s['roll_number']}")
        print(f"    Name        : {s['name']}")
        print(f"    Total Marks : {s['total']} / 500")
        print(f"    Percentage  : {s['percentage']}%")
        print(f"    Grade       : {s['grade']}")
        print(f"    Status      : {s['status']}")
        print("    Subject Breakdown:")
        for subj, mark in s.get("marks", {}).items():
            pass_indicator = "Pass" if mark >= 35.0 else "Fail"
            print(f"      - {subj:<18}: {mark:>5.1f} / 100 ({pass_indicator})")
        print("  " + "-" * 48)
