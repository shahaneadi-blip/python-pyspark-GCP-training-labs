products = []


def text(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("This value is required.")


def number(label, integer=False, minimum=0):
    while True:
        try:
            value = int(input(label)) if integer else float(input(label))
            if value < minimum:
                raise ValueError
            return value
        except ValueError:
            print(f"Enter a number not below {minimum}.")


def find_product(product_id):
    return next((product for product in products if product["id"] == product_id), None)


def display(product):
    print(f"ID: {product['id']} | {product['name']} | Category: {product['category']} | Price: {product['price']:.2f} | Quantity: {product['quantity']}")


def add_product():
    product_id = text("Product ID: ")
    if find_product(product_id):
        print("Product ID already exists.")
        return
    products.append({
        "id": product_id,
        "name": text("Product name: "),
        "category": text("Category: "),
        "price": number("Price: "),
        "quantity": number("Quantity: ", integer=True),
    })
    print("Product added.")


def view_inventory():
    if not products:
        print("Inventory is empty.")
        return
    for product in products:
        display(product)


def search_product():
    product = find_product(text("Product ID: "))
    if product:
        display(product)
    else:
        print("Product not found.")


def update_product():
    product = find_product(text("Product ID: "))
    if not product:
        print("Product not found.")
        return
    category = input(f"Category [{product['category']}]: ").strip()
    price = input(f"Price [{product['price']}]: ").strip()
    quantity = input(f"Quantity [{product['quantity']}]: ").strip()
    if category:
        product["category"] = category
    try:
        if price:
            product["price"] = float(price)
        if quantity:
            product["quantity"] = int(quantity)
        if product["price"] < 0 or product["quantity"] < 0:
            raise ValueError
    except ValueError:
        print("Invalid numeric update ignored.")
    print("Product updated.")


def delete_product():
    product = find_product(text("Product ID: "))
    if product:
        products.remove(product)
        print("Product deleted.")
    else:
        print("Product not found.")


def sell_product():
    product = find_product(text("Product ID: "))
    if not product:
        print("Product not found.")
        return
    quantity = number("Quantity to sell: ", integer=True, minimum=1)
    if quantity > product["quantity"]:
        print("Insufficient stock.")
        return
    product["quantity"] -= quantity
    print(f"Sale complete. Amount: {quantity * product['price']:.2f}")


def inventory_value():
    print(f"Inventory value: {sum(product['price'] * product['quantity'] for product in products):.2f}")


def low_stock():
    threshold = number("Low-stock threshold [10]: ", integer=True) if input("Use another threshold? (y/N): ").strip().lower() == "y" else 10
    matches = [product for product in products if product["quantity"] < threshold]
    if not matches:
        print("No low-stock products.")
    for product in matches:
        display(product)


def main():
    actions = {"1": add_product, "2": view_inventory, "3": search_product, "4": update_product, "5": delete_product, "6": sell_product, "7": inventory_value, "8": low_stock}
    while True:
        print("\n1 Add  2 View  3 Search  4 Update  5 Delete  6 Sell  7 Value  8 Low stock  9 Exit")
        choice = input("Choice: ").strip()
        if choice == "9":
            return
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
