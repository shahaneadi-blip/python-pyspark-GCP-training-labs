def main():
    try:
        first = float(input("First number: "))
        operator = input("Operator (+, -, *, /): ").strip()
        second = float(input("Second number: "))
        if operator == "+":
            result = first + second
        elif operator == "-":
            result = first - second
        elif operator == "*":
            result = first * second
        elif operator == "/" and second != 0:
            result = first / second
        else:
            print("Invalid operation.")
            return
        print(f"Result: {result}")
    except ValueError:
        print("Enter valid numbers.")


if __name__ == "__main__":
    main()
