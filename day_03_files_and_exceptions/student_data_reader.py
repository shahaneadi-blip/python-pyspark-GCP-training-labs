import csv
from collections import defaultdict
from pathlib import Path


class InvalidStudentRecordError(Exception):
    pass


BASE_DIR = Path(__file__).parent
REQUIRED_COLUMNS = {"student_id", "name", "course", "python", "sql", "cloud"}


def grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


def validate(row, seen_ids):
    if not REQUIRED_COLUMNS.issubset(row):
        raise InvalidStudentRecordError("Missing required columns")
    student_id = row["student_id"].strip()
    if not student_id:
        raise InvalidStudentRecordError("Missing student ID")
    if student_id in seen_ids:
        raise InvalidStudentRecordError("Duplicate student ID")
    if not row["name"].strip() or not row["course"].strip():
        raise InvalidStudentRecordError("Missing name or course")
    try:
        marks = [float(row[key]) for key in ("python", "sql", "cloud")]
    except ValueError as error:
        raise InvalidStudentRecordError("Marks must be numeric") from error
    if any(mark < 0 or mark > 100 for mark in marks):
        raise InvalidStudentRecordError("Marks must be between 0 and 100")
    seen_ids.add(student_id)
    percentage = sum(marks) / len(marks)
    return {"student_id": student_id, "name": row["name"].strip(), "course": row["course"].strip(), "python": marks[0], "sql": marks[1], "cloud": marks[2], "total": sum(marks), "percentage": percentage, "grade": grade(percentage), "result": "Pass" if percentage >= 50 else "Fail"}


def load_students(path):
    students, invalid, seen_ids = [], [], set()
    with path.open(newline="", encoding="utf-8") as file:
        for number, row in enumerate(csv.DictReader(file), 2):
            try:
                students.append(validate(row, seen_ids))
            except InvalidStudentRecordError as error:
                invalid.append((number, row, str(error)))
    return students, invalid


def course_statistics(students):
    groups = defaultdict(list)
    for student in students:
        groups[student["course"]].append(student)
    return {course: {"count": len(items), "average": sum(item["percentage"] for item in items) / len(items), "highest": max(item["percentage"] for item in items), "lowest": min(item["percentage"] for item in items), "passed": sum(item["result"] == "Pass" for item in items), "failed": sum(item["result"] == "Fail" for item in items)} for course, items in groups.items()}


def write_report(students, invalid):
    report = BASE_DIR / "student_report.txt"
    stats = course_statistics(students)
    top = max(students, key=lambda student: student["percentage"], default=None)
    lines = ["STUDENT PERFORMANCE REPORT", f"Valid records: {len(students)}", f"Invalid records: {len(invalid)}", "Students:"]
    lines.extend(f"{student['student_id']} | {student['name']} | {student['course']} | {student['percentage']:.2f}% | {student['grade']} | {student['result']}" for student in students)
    lines.append("Course statistics:")
    lines.extend(f"{course}: count={data['count']}, average={data['average']:.2f}, highest={data['highest']:.2f}, lowest={data['lowest']:.2f}, pass={data['passed']}, fail={data['failed']}" for course, data in stats.items())
    if top:
        lines.append(f"Top performer: {top['student_id']} | {top['name']} | {top['percentage']:.2f}% | {top['grade']}")
    lines.append("Failed students:")
    lines.extend(f"{student['student_id']} | {student['name']}" for student in students if student["result"] == "Fail")
    lines.append("Invalid records:")
    lines.extend(f"Line {number}: {reason} | {row}" for number, row, reason in invalid)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def show_students(students):
    for student in students:
        print(f"{student['student_id']} | {student['name']} | {student['course']} | {student['percentage']:.2f}% | {student['grade']} | {student['result']}")


def main():
    requested = input("Student CSV path [students.csv]: ").strip()
    path = Path(requested) if requested else BASE_DIR / "students.csv"
    try:
        students, invalid = load_students(path)
    except FileNotFoundError:
        print("Student file not found.")
        return
    report = write_report(students, invalid)
    while True:
        print("\n1 View  2 Search ID  3 Search name  4 Top performer  5 Failed students  6 Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            show_students(students)
        elif choice == "2":
            show_students([student for student in students if student["student_id"] == input("Student ID: ").strip()])
        elif choice == "3":
            query = input("Name: ").strip().lower()
            show_students([student for student in students if query in student["name"].lower()])
        elif choice == "4":
            show_students([max(students, key=lambda student: student["percentage"])]) if students else print("No valid students.")
        elif choice == "5":
            show_students([student for student in students if student["result"] == "Fail"])
        elif choice == "6":
            print(f"Report created: {report.name}")
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
