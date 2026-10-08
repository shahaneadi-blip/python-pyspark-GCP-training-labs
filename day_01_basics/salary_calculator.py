def calculate_salary(basic_salary, hra_rate, da_rate, tax_rate):
    hra = basic_salary * hra_rate / 100
    da = basic_salary * da_rate / 100
    gross = basic_salary + hra + da
    tax = gross * tax_rate / 100
    return hra, da, gross, tax, gross - tax


def main():
    basic = float(input("Basic salary: "))
    hra_rate = float(input("HRA percentage: "))
    da_rate = float(input("DA percentage: "))
    tax_rate = float(input("Tax percentage: "))
    hra, da, gross, tax, net = calculate_salary(basic, hra_rate, da_rate, tax_rate)
    print(f"HRA: {hra:.2f}\nDA: {da:.2f}\nGross: {gross:.2f}\nTax: {tax:.2f}\nNet salary: {net:.2f}")


if __name__ == "__main__":
    main()
