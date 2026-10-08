import pandas as pd


def analyse(products):
    frame = pd.DataFrame(products)
    if frame.empty:
        return frame, {}
    frame["inventory_value"] = frame["quantity"] * frame["purchase_price"]
    frame["sales_value"] = frame["quantity"] * frame["selling_price"]
    frame["potential_profit"] = (frame["selling_price"] - frame["purchase_price"]) * frame["quantity"]
    summary = {
        "total_products": len(frame),
        "total_quantity": int(frame["quantity"].sum()),
        "inventory_value": float(frame["inventory_value"].sum()),
        "sales_value": float(frame["sales_value"].sum()),
        "potential_profit": float(frame["potential_profit"].sum()),
        "category_quantity": frame.groupby("category")["quantity"].sum().sort_values(ascending=False),
        "valuable_products": frame.nlargest(5, "inventory_value")[["product_id", "product_name", "inventory_value"]],
    }
    return frame, summary


def print_analytics(products):
    _, summary = analyse(products)
    if not summary:
        print("No products available.")
        return
    print(f"Products: {summary['total_products']}")
    print(f"Quantity: {summary['total_quantity']}")
    print(f"Inventory value: {summary['inventory_value']:.2f}")
    print(f"Potential sales value: {summary['sales_value']:.2f}")
    print(f"Potential profit: {summary['potential_profit']:.2f}")
    print("Category quantities:")
    print(summary["category_quantity"])
    print("Most valuable products:")
    print(summary["valuable_products"].to_string(index=False))
