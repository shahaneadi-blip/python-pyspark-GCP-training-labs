import requests


def main():
    url = input("API URL [https://jsonplaceholder.typicode.com/posts/1]: ").strip() or "https://jsonplaceholder.typicode.com/posts/1"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        print(response.json())
    except requests.RequestException as error:
        print(f"Request failed: {error}")
    except ValueError:
        print(response.text)


if __name__ == "__main__":
    main()
