class Book:
    def __init__(self, isbn, title, author):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.borrower = None

    @property
    def available(self):
        return self.borrower is None

    def __str__(self):
        status = "Available" if self.available else f"Issued to {self.borrower}"
        return f"{self.isbn} | {self.title} | {self.author} | {status}"


class Library:
    def __init__(self):
        self.books = {}

    def add_book(self):
        isbn = input("ISBN: ").strip()
        if not isbn or isbn in self.books:
            print("Use a unique ISBN.")
            return
        self.books[isbn] = Book(isbn, input("Title: ").strip(), input("Author: ").strip())
        print("Book added.")

    def list_books(self):
        for book in self.books.values():
            print(book)
        if not self.books:
            print("No books found.")

    def search(self):
        query = input("Title or author: ").strip().lower()
        matches = [book for book in self.books.values() if query in book.title.lower() or query in book.author.lower()]
        for book in matches:
            print(book)
        if not matches:
            print("No matching books.")

    def issue(self):
        book = self.books.get(input("ISBN: ").strip())
        if not book:
            print("Book not found.")
        elif not book.available:
            print("Book is already issued.")
        else:
            book.borrower = input("Borrower: ").strip()
            print("Book issued.")

    def return_book(self):
        book = self.books.get(input("ISBN: ").strip())
        if not book:
            print("Book not found.")
        elif book.available:
            print("Book is already available.")
        else:
            book.borrower = None
            print("Book returned.")


def main():
    library = Library()
    actions = {"1": library.add_book, "2": library.list_books, "3": library.search, "4": library.issue, "5": library.return_book}
    while True:
        print("\n1 Add  2 View  3 Search  4 Issue  5 Return  6 Exit")
        choice = input("Choice: ").strip()
        if choice == "6":
            return
        if choice in actions:
            actions[choice]()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
