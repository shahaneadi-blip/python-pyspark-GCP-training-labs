class Employee:
    def __init__(self, employee_id, name, department, designation, salary):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.designation = designation
        self.salary = salary

    def update(self, department, designation, salary):
        self.department = department or self.department
        self.designation = designation or self.designation
        if salary:
            self.salary = float(salary)

    def __str__(self):
        return f"{self.employee_id} | {self.name} | {self.department} | {self.designation} | {self.salary:.2f}"


class EmployeeManagementSystem:
    def __init__(self):
        self.employees = {}

    def add(self):
        employee_id = input("Employee ID: ").strip()
        if not employee_id or employee_id in self.employees:
            print("Use a unique employee ID.")
            return
        try:
            self.employees[employee_id] = Employee(employee_id, input("Name: ").strip(), input("Department: ").strip(), input("Designation: ").strip(), float(input("Salary: ")))
            print("Employee added.")
        except ValueError:
            print("Salary must be numeric.")

    def view(self):
        for employee in self.employees.values():
            print(employee)
        if not self.employees:
            print("No employees found.")

    def search(self):
        query = input("ID, name, or department: ").strip().lower()
        matches = [employee for employee in self.employees.values() if query in employee.employee_id.lower() or query in employee.name.lower() or query in employee.department.lower()]
        for employee in matches:
            print(employee)
        if not matches:
            print("No employees found.")

    def update(self):
        employee = self.employees.get(input("Employee ID: ").strip())
        if not employee:
            print("Employee not found.")
            return
        try:
            employee.update(input("Department [keep]: ").strip(), input("Designation [keep]: ").strip(), input("Salary [keep]: ").strip())
            print("Employee updated.")
        except ValueError:
            print("Salary was not updated.")

    def delete(self):
        employee_id = input("Employee ID: ").strip()
        if self.employees.pop(employee_id, None):
            print("Employee deleted.")
        else:
            print("Employee not found.")


def main():
    system = EmployeeManagementSystem()
    actions = {"1": system.add, "2": system.view, "3": system.search, "4": system.update, "5": system.delete}
    while True:
        print("\n1 Add  2 View  3 Search  4 Update  5 Delete  6 Exit")
        choice = input("Choice: ").strip()
        if choice == "6":
            return
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
