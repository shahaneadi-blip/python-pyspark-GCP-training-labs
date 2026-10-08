RATES_FROM_INR = {"USD": 0.012, "EUR": 0.011, "GBP": 0.0095, "JPY": 1.78}


def main():
    amount = float(input("Amount in INR: "))
    currency = input("Target currency (USD/EUR/GBP/JPY): ").strip().upper()
    if currency not in RATES_FROM_INR:
        print("Unsupported currency.")
        return
    print(f"{amount:.2f} INR = {amount * RATES_FROM_INR[currency]:.2f} {currency}")


if __name__ == "__main__":
    main()
