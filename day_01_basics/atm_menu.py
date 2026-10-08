def amount(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
        except ValueError:
            pass
        print("Enter an amount greater than zero.")


def main():
    balance = 0.0
    while True:
        print("\n1 Deposit\n2 Withdraw\n3 Check balance\n4 Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            balance += amount("Deposit amount: ")
            print("Deposit successful.")
        elif choice == "2":
            withdrawal = amount("Withdrawal amount: ")
            if withdrawal > balance:
                print("Insufficient balance.")
            else:
                balance -= withdrawal
                print("Withdrawal successful.")
        elif choice == "3":
            print(f"Balance: {balance:.2f}")
        elif choice == "4":
            print("Thank you.")
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
