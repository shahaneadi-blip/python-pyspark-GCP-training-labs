from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).parent


def main():
    data = pd.read_csv(BASE_DIR / "sales.csv", parse_dates=["date"])
    data["revenue"] = data["quantity"] * data["unit_price"]
    print(f"Orders: {len(data)}")
    print(f"Revenue: {data['revenue'].sum():.2f}")
    print("\nRevenue by category")
    print(data.groupby("category")["revenue"].sum().sort_values(ascending=False).round(2))
    print("\nRevenue by region")
    print(data.groupby("region")["revenue"].sum().sort_values(ascending=False).round(2))
    output = BASE_DIR / "charts"
    output.mkdir(exist_ok=True)
    category_sales = data.groupby("category")["revenue"].sum().sort_values()
    figure, axis = plt.subplots(figsize=(8, 5))
    category_sales.plot.barh(ax=axis, color="#0f766e")
    axis.set(title="Revenue by Category", xlabel="Revenue", ylabel="Category")
    figure.tight_layout()
    figure.savefig(output / "revenue_by_category.png")
    plt.close(figure)
    monthly_sales = data.groupby(data["date"].dt.to_period("M"))["revenue"].sum()
    figure, axis = plt.subplots(figsize=(8, 5))
    monthly_sales.plot.line(ax=axis, marker="o", color="#7c3aed")
    axis.set(title="Monthly Revenue", xlabel="Month", ylabel="Revenue")
    figure.tight_layout()
    figure.savefig(output / "monthly_revenue.png")
    plt.close(figure)
    print(f"Charts created in {output}")


if __name__ == "__main__":
    main()
