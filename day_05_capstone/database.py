import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).parent
DATABASE = BASE_DIR / "inventory.db"
FIELDS = ("product_id", "product_name", "category", "quantity", "purchase_price", "selling_price", "supplier", "reorder_level", "date_added")


def connect():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row
    con.execute("CREATE TABLE IF NOT EXISTS products (product_id TEXT PRIMARY KEY, product_name TEXT NOT NULL, category TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity >= 0), purchase_price REAL NOT NULL CHECK(purchase_price >= 0), selling_price REAL NOT NULL CHECK(selling_price >= 0), supplier TEXT NOT NULL, reorder_level INTEGER NOT NULL CHECK(reorder_level >= 0), date_added TEXT NOT NULL)")
    return con


def validate(product):
    if not product["product_id"] or not product["product_name"] or not product["category"] or not product["supplier"] or not product["date_added"]:
        raise ValueError("Text fields are required")
    product["quantity"] = int(product["quantity"])
    product["purchase_price"] = float(product["purchase_price"])
    product["selling_price"] = float(product["selling_price"])
    product["reorder_level"] = int(product["reorder_level"])
    if any(product[field] < 0 for field in ("quantity", "purchase_price", "selling_price", "reorder_level")):
        raise ValueError("Numeric values cannot be negative")
    return product


def add_product(con, product):
    product = validate(product)
    con.execute(f"INSERT INTO products ({', '.join(FIELDS)}) VALUES ({', '.join('?' for _ in FIELDS)})", tuple(product[field] for field in FIELDS))
    con.commit()


def all_products(con):
    return [dict(row) for row in con.execute("SELECT * FROM products ORDER BY product_id")]


def search_products(con, query):
    term = f"%{query}%"
    return [dict(row) for row in con.execute("SELECT * FROM products WHERE product_id LIKE ? OR product_name LIKE ? OR category LIKE ? ORDER BY product_id", (term, term, term))]


def get_product(con, product_id):
    row = con.execute("SELECT * FROM products WHERE product_id = ?", (product_id,)).fetchone()
    return dict(row) if row else None


def update_product(con, product_id, product):
    product = validate(product)
    cursor = con.execute("UPDATE products SET product_name=?, category=?, quantity=?, purchase_price=?, selling_price=?, supplier=?, reorder_level=?, date_added=? WHERE product_id=?", (product["product_name"], product["category"], product["quantity"], product["purchase_price"], product["selling_price"], product["supplier"], product["reorder_level"], product["date_added"], product_id))
    con.commit()
    if not cursor.rowcount:
        raise LookupError("Product not found")


def delete_product(con, product_id):
    cursor = con.execute("DELETE FROM products WHERE product_id = ?", (product_id,))
    con.commit()
    return cursor.rowcount > 0


def low_stock_products(con):
    return [dict(row) for row in con.execute("SELECT * FROM products WHERE quantity <= reorder_level ORDER BY quantity, product_name")]
