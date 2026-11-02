"""
grade_calculator.py - Grade and marks calculation module.

This module provides functions to:
1. Validate marks input from the user (0 - 100 numeric range).
2. Calculate total marks and percentage across 5 subjects.
3. Determine letter grade according to the defined academic grading scale.
4. Determine pass or fail status based on subject-level and overall criteria.
"""

# Standard list of subjects for every student
SUBJECTS = ["Maths", "Science", "English", "Computer Science", "Social Studies"]

# Grade scale thresholds: tuple of (minimum_percentage, grade_letter)
GRADE_SCALE = [
    (90.0, "A+"),
    (80.0, "A"),
    (70.0, "B"),
    (60.0, "C"),
    (50.0, "D"),
    (0.0,  "F")
]

# Minimum marks required in each individual subject to pass
PASSING_SUBJECT_MARK = 35.0

# Minimum overall percentage required to pass
PASSING_PERCENTAGE = 50.0


def validate_mark_input(subject_name: str) -> float:
    """
    Prompt the user to enter marks for a specific subject and validate the input.

    Ensures the mark is numeric (integer or float) and falls strictly between 0 and 100.
    Continues to re-prompt until a valid value is provided.

    Args:
        subject_name (str): Name of the subject being prompted.

    Returns:
        float: Validated mark value rounded to 2 decimal places.
    """
    while True:
        try:
            raw_input = input(f"  Enter marks for {subject_name} (0-100): ").strip()
            if not raw_input:
                print("    [Error] Input cannot be empty. Please enter a valid number.")
                continue

            marks = float(raw_input)

            if 0.0 <= marks <= 100.0:
                return round(marks, 2)
            else:
                print(f"    [Error] Marks must be between 0 and 100. You entered: {marks}")

        except ValueError:
            print(f"    [Error] Invalid input '{raw_input}'. Please enter a numeric value (e.g. 85 or 92.5).")


def calculate_total(marks: dict) -> float:
    """
    Calculate the sum of all subject marks.

    Args:
        marks (dict): Dictionary mapping subject name to marks (e.g. {'Maths': 90}).

    Returns:
        float: Total marks rounded to 2 decimal places.
    """
    if not marks:
        return 0.0
    return round(sum(marks.values()), 2)


def calculate_percentage(total: float, subject_count: int = 5) -> float:
    """
    Calculate the percentage score based on total marks and number of subjects.

    Args:
        total (float): Sum of marks.
        subject_count (int): Number of subjects (default is 5).

    Returns:
        float: Percentage rounded to 2 decimal places.
    """
    if subject_count <= 0:
        return 0.0
    return round(total / subject_count, 2)


def determine_grade(percentage: float) -> str:
    """
    Determine the letter grade based on percentage.

    Grading Scale:
        A+ : 90 - 100
        A  : 80 - 89.99
        B  : 70 - 79.99
        C  : 60 - 69.99
        D  : 50 - 59.99
        F  : Below 50

    Args:
        percentage (float): Calculated percentage (0 - 100).

    Returns:
        str: Letter grade ("A+", "A", "B", "C", "D", or "F").
    """
    for threshold, grade in GRADE_SCALE:
        if percentage >= threshold:
            return grade
    return "F"


def determine_status(marks: dict, percentage: float) -> str:
    """
    Determine Pass or Fail status for a student.

    A student fails if:
    - Any subject mark is strictly below 35 (PASSING_SUBJECT_MARK).
    - Or overall percentage is strictly below 50 (PASSING_PERCENTAGE).

    Args:
        marks (dict): Dictionary mapping subject names to marks.
        percentage (float): Overall percentage.

    Returns:
        str: "Pass" if all conditions are met, otherwise "Fail".
    """
    for mark in marks.values():
        if mark < PASSING_SUBJECT_MARK:
            return "Fail"
    if percentage < PASSING_PERCENTAGE:
        return "Fail"
    return "Pass"


def calculate_student_result(marks: dict) -> tuple[float, float, str, str]:
    """
    Calculate total, percentage, grade, and pass/fail status from a marks dictionary.

    Args:
        marks (dict): Dictionary containing marks for all subjects.

    Returns:
        tuple[float, float, str, str]: (total, percentage, grade, status)
    """
    total = calculate_total(marks)
    count = len(marks) if marks else 5
    percentage = calculate_percentage(total, count)
    grade = determine_grade(percentage)
    status = determine_status(marks, percentage)
    return total, percentage, grade, status
