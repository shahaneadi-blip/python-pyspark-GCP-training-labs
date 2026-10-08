students = []


def read_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This value is required.")


def read_int(label, minimum=0, maximum=None):
    while True:
        try:
            value = int(input(label))
            if value < minimum or (maximum is not None and value > maximum):
                raise ValueError
            return value
        except ValueError:
            limit = f" between {minimum} and {maximum}" if maximum is not None else f" at least {minimum}"
            print(f"Enter a whole number{limit}.")


def find_student(student_id):
    return next((student for student in students if student["id"] == student_id), None)


def display_student(student):
    marks = student["marks"]
    total = sum(marks.values())
    average = total / len(marks)
    status = "Pass" if average >= 40 else "Fail"
    print(f"ID: {student['id']} | Name: {student['name']} | Age: {student['age']} | Course: {student['course']}")
    print(f"Python: {marks['python']} | SQL: {marks['sql']} | Azure: {marks['azure']} | Total: {total} | Average: {average:.2f} | {status}")


def add_student():
    student_id = read_nonempty("Student ID: ")
    if find_student(student_id):
        print("Student ID already exists.")
        return
    students.append({
        "id": student_id,
        "name": read_nonempty("Name: "),
        "age": read_int("Age: ", 1, 120),
        "course": read_nonempty("Course: "),
        "marks": {
            "python": read_int("Python marks: ", 0, 100),
            "sql": read_int("SQL marks: ", 0, 100),
            "azure": read_int("Azure marks: ", 0, 100),
        },
    })
    print("Student added.")


def view_students():
    if not students:
        print("No student records found.")
        return
    for student in students:
        display_student(student)


def search_student():
    student = find_student(read_nonempty("Student ID: "))
    if student:
        display_student(student)
    else:
        print("Student not found.")


def update_student():
    student = find_student(read_nonempty("Student ID: "))
    if not student:
        print("Student not found.")
        return
    name = input(f"Name [{student['name']}]: ").strip()
    age = input(f"Age [{student['age']}]: ").strip()
    course = input(f"Course [{student['course']}]: ").strip()
    if name:
        student["name"] = name
    if age:
        try:
            student["age"] = int(age)
        except ValueError:
            print("Age was not changed.")
    if course:
        student["course"] = course
    print("Student updated.")


def delete_student():
    student = find_student(read_nonempty("Student ID: "))
    if student:
        students.remove(student)
        print("Student deleted.")
    else:
        print("Student not found.")


def calculate_result():
    student = find_student(read_nonempty("Student ID: "))
    if student:
        display_student(student)
    else:
        print("Student not found.")


def highest_scorer():
    if not students:
        print("No student records found.")
        return
    student = max(students, key=lambda item: sum(item["marks"].values()) / len(item["marks"]))
    print("Highest scorer")
    display_student(student)


def main():
    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": calculate_result,
        "7": highest_scorer,
    }
    while True:
        print("\n1 Add  2 View  3 Search  4 Update  5 Delete  6 Result  7 Highest scorer  8 Exit")
        choice = input("Choice: ").strip()
        if choice == "8":
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
