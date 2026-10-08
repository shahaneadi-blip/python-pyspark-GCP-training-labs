import sqlite3
from pathlib import Path


DATABASE = Path(__file__).with_name("employees.db")


def connection():
    con = sqlite3.connect(DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS employees (employee_id TEXT PRIMARY KEY, name TEXT NOT NULL, department TEXT NOT NULL, designation TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, salary REAL NOT NULL CHECK(salary >= 0), joining_date TEXT NOT NULL)")
    return con


def display(rows):
    for row in rows:
        print(" | ".join(str(value) for value in row))
    if not rows:
        print("No employees found.")


def add(con):
    values = [input(f"{label}: ").strip() for label in ("Employee ID", "Name", "Department", "Designation", "Email", "Phone", "Salary", "Joining date YYYY-MM-DD")]
    try:
        values[6] = float(values[6])
        con.execute("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?, ?)", values)
        con.commit()
        print("Employee added.")
    except (ValueError, sqlite3.IntegrityError) as error:
        print(f"Employee not added: {error}")


def view(con):
    display(con.execute("SELECT * FROM employees ORDER BY employee_id").fetchall())


def search(con):
    query = input("ID, name, or department: ").strip()
    display(con.execute("SELECT * FROM employees WHERE employee_id = ? OR name LIKE ? OR department LIKE ? ORDER BY employee_id", (query, f"%{query}%", f"%{query}%")).fetchall())


def update(con):
    employee_id = input("Employee ID: ").strip()
    row = con.execute("SELECT * FROM employees WHERE employee_id = ?", (employee_id,)).fetchone()
    if not row:
        print("Employee not found.")
        return
    columns = ["name", "department", "designation", "email", "phone", "salary"]
    values = []
    for column, current in zip(columns, row[1:7]):
        value = input(f"{column.title()} [{current}]: ").strip()
        values.append(value if value else current)
    try:
        values[-1] = float(values[-1])
        con.execute("UPDATE employees SET name=?, department=?, designation=?, email=?, phone=?, salary=? WHERE employee_id=?", (*values, employee_id))
        con.commit()
        print("Employee updated.")
    except ValueError:
        print("Invalid salary.")


def delete(con):
    cursor = con.execute("DELETE FROM employees WHERE employee_id = ?", (input("Employee ID: ").strip(),))
    con.commit()
    print("Employee deleted." if cursor.rowcount else "Employee not found.")


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
