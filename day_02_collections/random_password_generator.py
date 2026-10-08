import secrets
import string


def generate_password(length):
    if length < 8:
        raise ValueError("Use at least 8 characters")
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if any(char.islower() for char in password) and any(char.isupper() for char in password) and any(char.isdigit() for char in password) and any(char in string.punctuation for char in password):
            return password


def main():
    try:
        print(generate_password(int(input("Password length: "))))
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()
