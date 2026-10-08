def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9


def main():
    value = float(input("Temperature value: "))
    unit = input("Unit (C/F): ").strip().upper()
    if unit == "C":
        print(f"{value:.2f} C = {celsius_to_fahrenheit(value):.2f} F")
    elif unit == "F":
        print(f"{value:.2f} F = {fahrenheit_to_celsius(value):.2f} C")
    else:
        print("Enter C or F.")


if __name__ == "__main__":
    main()
