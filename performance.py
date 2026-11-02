"""
performance.py - Performance summary and analytics module.

This module computes and formats key performance metrics for the class:
1. Class average percentage
2. Highest scorer(s) and lowest scorer(s)
3. Grade distribution (count of students in A+, A, B, C, D, F)
4. Overall pass percentage and pass/fail counts
5. Subject-wise average marks across all 5 subjects
"""

from grade_calculator import SUBJECTS


def calculate_class_average(students: list) -> float:
    """
    Calculate the average percentage across all students.

    Args:
        students (list): List of student dictionaries.

    Returns:
        float: Average percentage rounded to 2 decimal places, or 0.0 if empty.
    """
    if not students:
        return 0.0
    total_percentage = sum(s["percentage"] for s in students)
    return round(total_percentage / len(students), 2)


def find_highest_scorer(students: list) -> dict | None:
    """
    Find the student with the highest percentage.

    Args:
        students (list): List of student dictionaries.

    Returns:
        dict | None: The student dictionary with maximum percentage, or None if empty.
    """
    if not students:
        return None
    return max(students, key=lambda s: s["percentage"])


def find_lowest_scorer(students: list) -> dict | None:
    """
    Find the student with the lowest percentage.

    Args:
        students (list): List of student dictionaries.

    Returns:
        dict | None: The student dictionary with minimum percentage, or None if empty.
    """
    if not students:
        return None
    return min(students, key=lambda s: s["percentage"])


def calculate_grade_distribution(students: list) -> dict:
    """
    Count the number of students who achieved each grade (A+, A, B, C, D, F).

    Args:
        students (list): List of student dictionaries.

    Returns:
        dict: Mapping of grade string to student count.
    """
    distribution = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for s in students:
        grade = s.get("grade", "F")
        if grade in distribution:
            distribution[grade] += 1
        else:
            distribution["F"] += 1
    return distribution


def calculate_pass_percentage(students: list) -> tuple[float, int, int]:
    """
    Calculate the percentage of students who passed the examination.

    Args:
        students (list): List of student dictionaries.

    Returns:
        tuple[float, int, int]: (pass_percentage, passed_count, failed_count)
    """
    if not students:
        return 0.0, 0, 0

    passed_count = sum(1 for s in students if s.get("status") == "Pass")
    total_count = len(students)
    failed_count = total_count - passed_count
    pass_pct = round((passed_count / total_count) * 100, 2)
    return pass_pct, passed_count, failed_count


def calculate_subject_averages(students: list) -> dict:
    """
    Calculate the average marks obtained in each subject.

    Args:
        students (list): List of student dictionaries.

    Returns:
        dict: Mapping of subject name to average mark rounded to 2 decimal places.
    """
    if not students:
        return {subject: 0.0 for subject in SUBJECTS}

    subject_totals = {subject: 0.0 for subject in SUBJECTS}
    total_students = len(students)

    for s in students:
        marks = s.get("marks", {})
        for subject in SUBJECTS:
            subject_totals[subject] += marks.get(subject, 0.0)

    return {
        subject: round(subject_totals[subject] / total_students, 2)
        for subject in SUBJECTS
    }


def display_performance_summary(students: list) -> None:
    """
    Display a comprehensive, neatly formatted class performance report.

    Includes class average, toppers, lowest scorers, pass percentage,
    grade distribution with visual bar representation, and subject averages.

    Args:
        students (list): List of student dictionaries.
    """
    print("\n" + "=" * 68)
    print("                 CLASS PERFORMANCE SUMMARY REPORT")
    print("=" * 68)

    if not students:
        print("  [Info] No student records available to analyze.")
        print("  Please add student records first from the main menu.")
        print("=" * 68)
        return

    total_count = len(students)
    class_avg = calculate_class_average(students)
    pass_rate, pass_count, fail_count = calculate_pass_percentage(students)
    topper = find_highest_scorer(students)
    lowest = find_lowest_scorer(students)
    distribution = calculate_grade_distribution(students)
    subject_averages = calculate_subject_averages(students)

    # 1. Overview Metrics
    print(f"  Total Students Enrolled : {total_count}")
    print(f"  Class Average Percentage: {class_avg}%")
    print(f"  Overall Pass Percentage : {pass_rate}% ({pass_count} Passed, {fail_count} Failed)")
    print("-" * 68)

    # 2. Topper and Lowest Scorer
    if topper:
        print("  TOP PERFORMER (Highest Scorer):")
        print(f"    * Name       : {topper['name']}")
        print(f"    * Roll Number: {topper['roll_number']}")
        print(f"    * Score      : {topper['total']}/500 ({topper['percentage']}%) - Grade {topper['grade']}")

    if lowest:
        print("\n  LOWEST PERFORMER:")
        print(f"    - Name       : {lowest['name']}")
        print(f"    - Roll Number: {lowest['roll_number']}")
        print(f"    - Score      : {lowest['total']}/500 ({lowest['percentage']}%) - Grade {lowest['grade']} [{lowest['status']}]")

    # 3. Grade Distribution with text bars
    print("-" * 68)
    print("  GRADE DISTRIBUTION:")
    scale_legend = {
        "A+": "90 - 100%",
        "A":  "80 - 89.9%",
        "B":  "70 - 79.9%",
        "C":  "60 - 69.9%",
        "D":  "50 - 59.9%",
        "F":  "< 50% (Fail)"
    }
    max_bar_width = 20
    for grade, count in distribution.items():
        proportion = count / total_count if total_count > 0 else 0
        bar_len = int(round(proportion * max_bar_width))
        bar = "#" * bar_len + " " * (max_bar_width - bar_len)
        percentage_str = f"{(proportion * 100):>5.1f}%"
        print(f"    {grade:<2} ({scale_legend[grade]:<12}) : [{bar}] {count:>2} student(s) ({percentage_str})")

    # 4. Subject-Wise Average Marks
    print("-" * 68)
    print("  SUBJECT-WISE AVERAGE MARKS (Out of 100):")
    print(f"    {'Subject':<20} | {'Class Average':>15}")
    print("    " + "-" * 20 + "-+-" + "-" * 15)
    for subject in SUBJECTS:
        avg_val = subject_averages.get(subject, 0.0)
        print(f"    {subject:<20} | {avg_val:>13.2f} ")

    print("=" * 68)
