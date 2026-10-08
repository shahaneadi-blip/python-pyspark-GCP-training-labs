class InsufficientFundsError(Exception):
    pass


class BankAccount:
    def __init__(self, account_number, holder, opening_balance=0):
        self.account_number = account_number
        self.holder = holder
        self.__balance = opening_balance
        self.transactions = [("Opening balance", opening_balance)]

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.__balance += amount
        self.transactions.append(("Deposit", amount))

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise InsufficientFundsError("Insufficient balance")
        self.__balance -= amount
        self.transactions.append(("Withdrawal", -amount))

    def __str__(self):
        return f"{self.account_number} | {self.holder} | Balance: {self.balance:.2f}"


class Bank:
    def __init__(self):
        self.accounts = {}

    def create(self):
        account_number = input("Account number: ").strip()
        if not account_number or account_number in self.accounts:
            print("Use a unique account number.")
            return
        try:
            self.accounts[account_number] = BankAccount(account_number, input("Account holder: ").strip(), float(input("Opening balance: ") or 0))
            print("Account created.")
        except ValueError:
            print("Invalid opening balance.")

    def account(self):
        account = self.accounts.get(input("Account number: ").strip())
        if not account:
            print("Account not found.")
        return account

    def deposit(self):
        account = self.account()
        if account:
            try:
                account.deposit(float(input("Amount: ")))
                print("Deposit successful.")
            except ValueError as error:
                print(error)

    def withdraw(self):
        account = self.account()
        if account:
            try:
                account.withdraw(float(input("Amount: ")))
                print("Withdrawal successful.")
            except (ValueError, InsufficientFundsError) as error:
                print(error)

    def statement(self):
        account = self.account()
        if account:
            print(account)
            for description, amount in account.transactions:
                print(f"{description}: {amount:.2f}")


def main():
    bank = Bank()
    actions = {"1": bank.create, "2": bank.deposit, "3": bank.withdraw, "4": bank.statement}
    while True:
        print("\n1 Create account  2 Deposit  3 Withdraw  4 Statement  5 Exit")
        choice = input("Choice: ").strip()
        if choice == "5":
            return
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
