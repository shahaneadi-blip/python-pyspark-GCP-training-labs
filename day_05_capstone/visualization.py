from pathlib import Path

import matplotlib.pyplot as plt

from analytics import analyse


def create_charts(products):
    frame, summary = analyse(products)
    if not summary:
        raise ValueError("No products available")
    output = Path(__file__).with_name("charts")
    output.mkdir(exist_ok=True)
    figure, axis = plt.subplots(figsize=(9, 5))
    axis.bar(frame["product_name"], frame["quantity"], color="#2563eb")
    axis.set(title="Product Quantity", xlabel="Product", ylabel="Quantity")
    axis.tick_params(axis="x", rotation=35)
    figure.tight_layout()
    figure.savefig(output / "product_quantity.png")
    plt.close(figure)
    category_values = frame.groupby("category")["inventory_value"].sum()
    figure, axis = plt.subplots(figsize=(7, 7))
    axis.pie(category_values, labels=category_values.index, autopct="%1.1f%%")
    axis.set_title("Inventory Value by Category")
    figure.tight_layout()
    figure.savefig(output / "category_inventory_value.png")
    plt.close(figure)
    return output
