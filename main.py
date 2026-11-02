"""
main.py - Main entry point and menu-driven CLI for Student Result & Grade Management System.

This module provides the interactive command-line interface (CLI) loop,
routes user choices to the corresponding operations, and ensures robust exception
handling so the application never crashes unexpectedly.
"""

import os
import sys
from student_manager import (
    load_students,
    save_students,
    add_student,
    update_student,
    delete_student,
    view_all_students,
    search_student,
)
from performance import display_performance_summary

# Resolve path to data/students.json relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "students.json")


def display_menu() -> None:
    """Display the primary menu options for the CLI application."""
    print("\n" + "=" * 55)
    print("      STUDENT RESULT & GRADE MANAGEMENT SYSTEM")
    print("=" * 55)
    print("  1. Add Student")
    print("  2. Update Student")
    print("  3. Delete Student")
    print("  4. View All Students")
    print("  5. Search Student")
    print("  6. Performance Summary")
    print("  7. Exit")
    print("=" * 55)


def main() -> None:
    """
    Run the main menu-driven loop of the application.

    Loads existing student records on launch, processes menu choices,
    and ensures records are saved upon exit or interruption.
    """
    print("\n" + "*" * 55)
    print(" Welcome to Student Result & Grade Management System")
    print("*" * 55)

    # Load persistent records from data/students.json
    students = load_students(DATA_FILE)
    print(f"Loaded {len(students)} student record(s) from 'data/{os.path.basename(DATA_FILE)}'.")

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-7, or 'q' to exit): ").strip()

            if choice in ("1", "add"):
                add_student(students, DATA_FILE)

            elif choice in ("2", "update"):
                update_student(students, DATA_FILE)

            elif choice in ("3", "delete"):
                delete_student(students, DATA_FILE)

            elif choice in ("4", "view"):
                view_all_students(students)

            elif choice in ("5", "search"):
                search_student(students)

            elif choice in ("6", "summary", "performance"):
                display_performance_summary(students)

            elif choice in ("7", "exit", "quit", "q"):
                print("\nSaving student records...")
                save_students(students, DATA_FILE)
                print("Thank you for using Student Result & Grade Management System.")
                print("Application closed successfully. Goodbye!\n")
                sys.exit(0)

            else:
                print(f"\n  [Error] '{choice}' is not a valid menu option.")
                print("  Please enter a number between 1 and 7.")

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\n[Notice] Program interrupted by user.")
            print("Auto-saving records before exit...")
            save_students(students, DATA_FILE)
            print("Goodbye!\n")
            sys.exit(0)

        except EOFError:
            # Handle EOF gracefully (e.g. redirected input streams)
            print("\n\n[Notice] Input stream ended. Auto-saving records...")
            save_students(students, DATA_FILE)
            sys.exit(0)

        except Exception as e:
            # Catch-all to prevent unhandled crashes
            print(f"\n  [Unexpected Error] An unexpected error occurred: {e}")
            print("  Returning to the main menu...\n")


if __name__ == "__main__":
    main()
