from datetime import date
from pathlib import Path
import sqlite3

from analytics import print_analytics
from database import FIELDS, add_product, all_products, connect, delete_product, get_product, low_stock_products, search_products, update_product
from file_handler import export_csv, import_csv, log_activity
from visualization import create_charts


def display(products):
    if not products:
        print("No products found.")
        return
    for product in products:
        print(f"{product['product_id']} | {product['product_name']} | {product['category']} | Quantity: {product['quantity']} | Cost: {product['purchase_price']:.2f} | Price: {product['selling_price']:.2f} | Reorder: {product['reorder_level']}")


def product_input(existing=None):
    existing = existing or {}
    product = {}
    for field in FIELDS:
        if field == "product_id" and existing:
            product[field] = existing[field]
            continue
        default = str(existing.get(field, date.today().isoformat() if field == "date_added" else ""))
        value = input(f"{field.replace('_', ' ').title()} [{default}]: ").strip()
        product[field] = value or default
    return product


def add(con):
    product = product_input()
    add_product(con, product)
    log_activity(f"Product {product['product_id']} added")
    print("Product added.")


def update(con):
    product_id = input("Product ID: ").strip()
    existing = get_product(con, product_id)
    if not existing:
        print("Product not found.")
        return
    product = product_input(existing)
    update_product(con, product_id, product)
    log_activity(f"Product {product_id} updated")
    print("Product updated.")


def remove(con):
    product_id = input("Product ID: ").strip()
    if input(f"Delete {product_id}? (y/N): ").strip().lower() == "y" and delete_product(con, product_id):
        log_activity(f"Product {product_id} deleted")
        print("Product deleted.")
    else:
        print("No product deleted.")


def main():
    con = connect()
    data_file = Path(__file__).parent / "data" / "products.csv"
    try:
        while True:
            print("\n1 Add  2 View  3 Search  4 Update  5 Delete  6 Import CSV  7 Export CSV  8 Low stock  9 Analytics  10 Charts  11 Exit")
            choice = input("Choice: ").strip()
            try:
                if choice == "1":
                    add(con)
                elif choice == "2":
                    display(all_products(con))
                elif choice == "3":
                    display(search_products(con, input("Search text: ").strip()))
                elif choice == "4":
                    update(con)
                elif choice == "5":
                    remove(con)
                elif choice == "6":
                    path = input(f"CSV path [{data_file}]: ").strip() or data_file
                    inserted, rejected = import_csv(con, path)
                    print(f"Imported: {inserted}; rejected: {len(rejected)}")
                    for line, reason in rejected:
                        print(f"Line {line}: {reason}")
                elif choice == "7":
                    print(f"Exported: {export_csv(all_products(con))}")
                elif choice == "8":
                    display(low_stock_products(con))
                elif choice == "9":
                    print_analytics(all_products(con))
                elif choice == "10":
                    print(f"Charts created: {create_charts(all_products(con))}")
                elif choice == "11":
                    return
                else:
                    print("Invalid choice.")
            except (ValueError, LookupError, sqlite3.Error, OSError) as error:
                print(f"Operation failed: {error}")
    finally:
        con.close()


if __name__ == "__main__":
    main()
