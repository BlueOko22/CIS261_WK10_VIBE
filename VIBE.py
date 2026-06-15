# David Gulley II
# CIS261
# VIBE Coding

import os
import sys

DATA_FILE = "student_grades.txt"

class Student:
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.test1 = float(test1)
        self.test2 = float(test2)
        self.test3 = float(test3)
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return round((self.test1 + self.test2 + self.test3) / 3.0, 2)

    def calculate_grade(self) -> str:
        if self.average >= 90:
            return "A"
        if self.average >= 80:
            return "B"
        if self.average >= 70:
            return "C"
        if self.average >= 60:
            return "D"
        return "F"

    def to_record(self) -> str:
        return f"{self.name}|{self.student_id}|{self.test1:.2f}|{self.test2:.2f}|{self.test3:.2f}|{self.average:.2f}|{self.grade}"

    @classmethod
    def from_record(cls, record_line: str):
        parts = record_line.strip().split("|")
        if len(parts) != 7:
            raise ValueError("Record does not contain 7 fields")

        name, student_id, test1, test2, test3, average, grade = parts
        student = cls(name, student_id, test1, test2, test3)

        if f"{student.average:.2f}" != f"{float(average):.2f}" or student.grade != grade:
            student.average = round((student.test1 + student.test2 + student.test3) / 3.0, 2)
            student.grade = student.calculate_grade()
        return student


def load_students(filename: str):
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if line.strip():
                    try:
                        student = Student.from_record(line)
                        students.append(student)
                    except Exception as error:
                        print(f"Warning: Skipping invalid record on line {line_number}: {error}")
    except IOError as error:
        print(f"Error loading records: {error}")
    return students


def save_students(filename: str, students):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
        print(f"Saved {len(students)} student record(s) to '{filename}'.")
    except IOError as error:
        print(f"Error saving records: {error}")


def input_float(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        if value.upper() == "ESC":
            raise KeyboardInterrupt
        try:
            return float(value)
        except ValueError:
            print("Invalid entry. Please enter a numeric value for the score.")


def add_student(students):
    print("\nAdd New Student Record")
    print("(Type ESC at any prompt to return to the main menu.)")
    try:
        name = input("Student name: ").strip()
        if name.upper() == "ESC":
            return

        student_id = input("Student ID: ").strip()
        if student_id.upper() == "ESC":
            return

        test1 = input_float("Test 1 score: ")
        test2 = input_float("Test 2 score: ")
        test3 = input_float("Test 3 score: ")
    except KeyboardInterrupt:
        print("\nReturning to main menu.")
        return

    student = Student(name, student_id, test1, test2, test3)
    students.append(student)
    print(f"Student '{student.name}' added with average {student.average:.2f} and grade {student.grade}.\n")


def display_students(students):
    if not students:
        print("\nNo student records available to display.\n")
        return

    header = f"{'Name':<20} | {'ID':<12} | {'Test 1':>7} | {'Test 2':>7} | {'Test 3':>7} | {'Average':>8} | {'Grade':>5}"
    separator = "-" * len(header)
    print("\nStudent Records")
    print(separator)
    print(header)
    print(separator)
    for student in students:
        print(
            f"{student.name:<20} | {student.student_id:<12} | {student.test1:7.2f} | {student.test2:7.2f} | {student.test3:7.2f} | {student.average:8.2f} | {student.grade:>5}"
        )
    print(separator + "\n")


def display_statistics(students):
    if not students:
        print("\nNo class statistics available because there are no student records.\n")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_average = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("----------------")
    print(f"Highest average: {highest:.2f}")
    print(f"Lowest average:  {lowest:.2f}")
    print(f"Class average:   {class_average:.2f}\n")


def search_student(students):
    if not students:
        print("\nNo student records available to search.\n")
        return

    search_name = input("Enter student name to search: ").strip()
    if not search_name:
        print("Please enter a name to search.\n")
        return

    found = [student for student in students if search_name.lower() in student.name.lower()]
    if not found:
        print(f"No students found matching '{search_name}'.\n")
        return

    print(f"\nSearch results for '{search_name}':")
    for student in found:
        print(
            f"- {student.name} (ID: {student.student_id}) | Test1: {student.test1:.2f} | Test2: {student.test2:.2f} | Test3: {student.test3:.2f} | Avg: {student.average:.2f} | Grade: {student.grade}"
        )
    print()


def print_menu():
    print("Student Grade Calculator")
    print("========================")
    print("1. Add new student record")
    print("2. Display all student records")
    print("3. Class statistics")
    print("4. Search student by name")
    print("5. Save records")
    print("ESC. Exit program")


def get_menu_choice():
    choice = input("Choose an option (1-5 or ESC to exit): ").strip()
    if choice == "":
        return None
    if choice.upper() == "ESC" or "\x1b" in choice:
        return "ESC"
    return choice


def main():
    students = load_students(DATA_FILE)
    if students:
        print(f"Loaded {len(students)} record(s) from '{DATA_FILE}'.\n")
    else:
        print(f"No existing student records found. Starting with an empty list.\n")

    while True:
        print_menu()
        choice = get_menu_choice()

        if choice == "ESC":
            print("Exiting the Student Grade Calculator. Goodbye!")
            break

        if choice == "1":
            add_student(students)
        elif choice == "2":
            display_students(students)
        elif choice == "3":
            display_statistics(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            save_students(DATA_FILE, students)
        else:
            print("Invalid choice. Please select 1-5 or type ESC to exit.\n")

    save_students(DATA_FILE, students)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted. Saving records before exit...")
        students = load_students(DATA_FILE)
        save_students(DATA_FILE, students)
        sys.exit(0)
