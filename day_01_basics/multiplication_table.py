def main():
    number = int(input("Number: "))
    limit = int(input("Limit: "))
    for multiplier in range(1, limit + 1):
        print(f"{number} x {multiplier} = {number * multiplier}")


if __name__ == "__main__":
    main()
