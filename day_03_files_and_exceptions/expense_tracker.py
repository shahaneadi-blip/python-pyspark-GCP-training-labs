import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class InvalidExpenseError(Exception):
    pass


BASE_DIR = Path(__file__).parent
CSV_PATH = BASE_DIR / "expenses.csv"
CATEGORIES = {"Food", "Transport", "Shopping", "Bills", "Entertainment", "Healthcare", "Education", "Other"}
PAYMENT_METHODS = {"Cash", "Card", "UPI", "Bank Transfer"}
FIELDS = ["expense_id", "date", "category", "description", "amount", "payment_method"]


def validate(row, identifiers):
    if any(not row.get(field, "").strip() for field in FIELDS):
        raise InvalidExpenseError("Missing required field")
    if row["expense_id"] in identifiers:
        raise InvalidExpenseError("Duplicate expense ID")
    try:
        date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        amount = float(row["amount"])
    except ValueError as error:
        raise InvalidExpenseError("Invalid date or amount") from error
    if amount <= 0:
        raise InvalidExpenseError("Amount must be positive")
    if row["category"] not in CATEGORIES or row["payment_method"] not in PAYMENT_METHODS:
        raise InvalidExpenseError("Invalid category or payment method")
    identifiers.add(row["expense_id"])
    return {**row, "date": date, "amount": amount}


def load_expenses():
    expenses, invalid, identifiers = [], [], set()
    if not CSV_PATH.exists():
        return expenses, invalid
    with CSV_PATH.open(newline="", encoding="utf-8") as file:
        for number, row in enumerate(csv.DictReader(file), 2):
            try:
                expenses.append(validate(row, identifiers))
            except InvalidExpenseError as error:
                invalid.append((number, row, str(error)))
    return expenses, invalid


def save_expenses(expenses):
    with CSV_PATH.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        for expense in expenses:
            writer.writerow({**expense, "date": expense["date"].isoformat(), "amount": f"{expense['amount']:.2f}"})


def display(expenses):
    if not expenses:
        print("No matching expenses.")
    for expense in expenses:
        print(f"{expense['expense_id']} | {expense['date']} | {expense['category']} | {expense['description']} | {expense['amount']:.2f} | {expense['payment_method']}")


def summary(expenses):
    if not expenses:
        print("No expenses available.")
        return
    amounts = [expense["amount"] for expense in expenses]
    print(f"Count: {len(expenses)} | Total: {sum(amounts):.2f} | Average: {sum(amounts) / len(amounts):.2f} | Highest: {max(amounts):.2f} | Lowest: {min(amounts):.2f}")


def grouped(expenses, field):
    values = defaultdict(float)
    for expense in expenses:
        values[expense[field]] += expense["amount"]
    for name, total in sorted(values.items()):
        print(f"{name}: {total:.2f}")


def read_new_expense(expenses):
    identifiers = {expense["expense_id"] for expense in expenses}
    row = {field: input(f"{field.replace('_', ' ').title()}: ").strip() for field in FIELDS}
    return validate(row, identifiers)


def report(expenses, invalid):
    path = BASE_DIR / "expense_report.txt"
    by_category = defaultdict(float)
    by_payment = defaultdict(float)
    for expense in expenses:
        by_category[expense["category"]] += expense["amount"]
        by_payment[expense["payment_method"]] += expense["amount"]
    lines = ["EXPENSE REPORT", f"Records: {len(expenses)}", f"Total: {sum(expense['amount'] for expense in expenses):.2f}", "Category summary:"]
    lines.extend(f"{key}: {value:.2f}" for key, value in sorted(by_category.items()))
    lines.append("Payment summary:")
    lines.extend(f"{key}: {value:.2f}" for key, value in sorted(by_payment.items()))
    if expenses:
        lines.append(f"Highest: {max(expenses, key=lambda expense: expense['amount'])['expense_id']}")
        lines.append(f"Lowest: {min(expenses, key=lambda expense: expense['amount'])['expense_id']}")
    lines.append("Invalid records:")
    lines.extend(f"Line {number}: {reason} | {row}" for number, row, reason in invalid)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main():
    expenses, invalid = load_expenses()
    while True:
        print("\n1 Add  2 View  3 Search  4 Total  5 Category  6 Payment  7 Month  8 Date range  9 Highest  10 Report  11 Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            try:
                expenses.append(read_new_expense(expenses))
                save_expenses(expenses)
                print("Expense saved.")
            except InvalidExpenseError as error:
                print(f"Expense not saved: {error}")
        elif choice == "2":
            display(expenses)
        elif choice == "3":
            query = input("Search text: ").strip().lower()
            display([expense for expense in expenses if query in " ".join(str(value).lower() for value in expense.values())])
        elif choice == "4":
            summary(expenses)
        elif choice == "5":
            grouped(expenses, "category")
        elif choice == "6":
            grouped(expenses, "payment_method")
        elif choice == "7":
            month = input("Month (YYYY-MM): ").strip()
            matches = [expense for expense in expenses if expense["date"].strftime("%Y-%m") == month]
            display(matches)
            summary(matches)
        elif choice == "8":
            try:
                start = datetime.strptime(input("Start date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                end = datetime.strptime(input("End date (YYYY-MM-DD): "), "%Y-%m-%d").date()
                matches = [expense for expense in expenses if start <= expense["date"] <= end]
                display(matches)
                summary(matches)
            except ValueError:
                print("Use YYYY-MM-DD dates.")
        elif choice == "9":
            display([max(expenses, key=lambda expense: expense["amount"])]) if expenses else print("No expenses available.")
        elif choice == "10":
            print(f"Report created: {report(expenses, invalid).name}")
        elif choice == "11":
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
