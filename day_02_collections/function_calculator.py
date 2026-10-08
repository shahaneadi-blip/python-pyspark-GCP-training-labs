def add(first, second):
    return first + second


def subtract(first, second):
    return first - second


def multiply(first, second):
    return first * second


def divide(first, second):
    if second == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return first / second


def main():
    operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
    try:
        first = float(input("First number: "))
        operator = input("Operator (+, -, *, /): ").strip()
        second = float(input("Second number: "))
        print(f"Result: {operations[operator](first, second)}")
    except (ValueError, KeyError, ZeroDivisionError) as error:
        print(error)


if __name__ == "__main__":
    main()
