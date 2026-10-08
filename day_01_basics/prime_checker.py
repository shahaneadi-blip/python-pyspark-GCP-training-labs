def is_prime(number):
    if number < 2:
        return False
    for divisor in range(2, int(number**0.5) + 1):
        if number % divisor == 0:
            return False
    return True


def main():
    number = int(input("Number: "))
    print(f"{number} is {'prime' if is_prime(number) else 'not prime'}.")


if __name__ == "__main__":
    main()
