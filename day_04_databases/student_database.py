import sqlite3
from pathlib import Path


DATABASE = Path(__file__).with_name("students.db")


def connection():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS students (student_id TEXT PRIMARY KEY, name TEXT NOT NULL, course TEXT NOT NULL, dob TEXT NOT NULL, gender TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100))")
    return con


def display(rows):
    for row in rows:
        percentage = row[-1]
        grade = "A+" if percentage >= 90 else "A" if percentage >= 80 else "B" if percentage >= 70 else "C" if percentage >= 60 else "D" if percentage >= 50 else "F"
        print(" | ".join(str(value) for value in row) + f" | {grade} | {'Pass' if percentage >= 50 else 'Fail'}")
    if not rows:
        print("No students found.")


def add(con):
    values = [input(f"{label}: ").strip() for label in ("Student ID", "Name", "Course", "Date of birth YYYY-MM-DD", "Gender", "Email", "Phone", "Marks")]
    try:
        values[-1] = float(values[-1])
        con.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        con.commit()
        print("Student added.")
    except (ValueError, sqlite3.IntegrityError) as error:
        print(f"Student not added: {error}")


def view(con):
    display(con.execute("SELECT * FROM students ORDER BY student_id").fetchall())


def search(con):
    query = input("ID, name, or course: ").strip()
    display(con.execute("SELECT * FROM students WHERE student_id=? OR name LIKE ? OR course LIKE ? ORDER BY student_id", (query, f"%{query}%", f"%{query}%")).fetchall())


def update(con):
    student_id = input("Student ID: ").strip()
    row = con.execute("SELECT * FROM students WHERE student_id=?", (student_id,)).fetchone()
    if not row:
        print("Student not found.")
        return
    columns = ["name", "course", "email", "phone", "marks"]
    positions = [1, 2, 5, 6, 7]
    values = []
    for column, position in zip(columns, positions):
        value = input(f"{column.title()} [{row[position]}]: ").strip()
        values.append(value if value else row[position])
    try:
        values[-1] = float(values[-1])
        con.execute("UPDATE students SET name=?, course=?, email=?, phone=?, marks=? WHERE student_id=?", (*values, student_id))
        con.commit()
        print("Student updated.")
    except ValueError:
        print("Marks must be numeric.")


def delete(con):
    cursor = con.execute("DELETE FROM students WHERE student_id=?", (input("Student ID: ").strip(),))
    con.commit()
    print("Student deleted." if cursor.rowcount else "Student not found.")


def main():
    con = connection()
    actions = {"1": add, "2": view, "3": search, "4": update, "5": delete}
    try:
        while True:
            print("\n1 Add  2 View  3 Search  4 Update  5 Delete  6 Exit")
            choice = input("Choice: ").strip()
            if choice == "6":
                return
            if choice in actions:
                actions[choice](con)
            else:
                print("Invalid choice.")
    finally:
        con.close()


if __name__ == "__main__":
    main()
