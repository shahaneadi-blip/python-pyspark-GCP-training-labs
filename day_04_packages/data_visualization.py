from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    data = pd.DataFrame({"category": ["Electronics", "Accessories", "Furniture", "Stationery"], "sales": [125000, 78000, 96000, 42000], "orders": [120, 260, 85, 310]})
    output = Path(__file__).with_name("charts")
    output.mkdir(exist_ok=True)
    figure, axis = plt.subplots(figsize=(8, 5))
    axis.bar(data["category"], data["sales"], color="#2563eb")
    axis.set(title="Sales by Category", xlabel="Category", ylabel="Sales")
    figure.tight_layout()
    figure.savefig(output / "sales_by_category.png")
    plt.close(figure)
    figure, axis = plt.subplots(figsize=(6, 6))
    axis.pie(data["orders"], labels=data["category"], autopct="%1.1f%%")
    axis.set_title("Order Distribution")
    figure.tight_layout()
    figure.savefig(output / "order_distribution.png")
    plt.close(figure)
    print(f"Charts created in {output}")


if __name__ == "__main__":
    main()
