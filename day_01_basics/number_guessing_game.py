import random


def main():
    target = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Guess a number from 1 to 100: "))
        except ValueError:
            print("Enter a whole number.")
            continue
        attempts += 1
        if guess < target:
            print("Too low.")
        elif guess > target:
            print("Too high.")
        else:
            print(f"Correct in {attempts} attempts.")
            return


if __name__ == "__main__":
    main()
