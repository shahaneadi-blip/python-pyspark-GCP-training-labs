from pathlib import Path

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, dense_rank, desc, row_number, sum as spark_sum


BASE_DIR = Path(__file__).parent


def main():
    spark = SparkSession.builder.appName("RetailSalesAnalytics").master("local[*]").getOrCreate()
    try:
        customers = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "customers.csv"))
        products = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "products.csv"))
        sales = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "sales.csv"))
        enriched = sales.join(customers.select("customer_id", "customer_name", "city"), "customer_id", "left").join(products, "product_id", "left").withColumn("revenue", col("quantity") * col("unit_price"))
        customer_window = Window.partitionBy("customer_id").orderBy("sale_date", "sale_id").rowsBetween(Window.unboundedPreceding, Window.currentRow)
        category_window = Window.partitionBy("category").orderBy(desc("revenue"))
        analysed = enriched.withColumn("running_customer_revenue", spark_sum("revenue").over(customer_window)).withColumn("category_sale_rank", dense_rank().over(category_window)).withColumn("customer_sale_number", row_number().over(Window.partitionBy("customer_id").orderBy("sale_date", "sale_id")))
        category_report = analysed.groupBy("category").agg(spark_sum("quantity").alias("units_sold"), spark_sum("revenue").alias("revenue")).orderBy(desc("revenue"))
        product_report = analysed.groupBy("product_id", "product_name", "category").agg(spark_sum("quantity").alias("units_sold"), spark_sum("revenue").alias("revenue")).withColumn("product_rank", dense_rank().over(Window.partitionBy("category").orderBy(desc("revenue")))).orderBy("category", "product_rank")
        print("Enriched sales with window metrics")
        analysed.orderBy("sale_id").show(truncate=False)
        print("Category performance")
        category_report.show(truncate=False)
        print("Product performance")
        product_report.show(truncate=False)
        output = BASE_DIR / "output"
        category_report.write.mode("overwrite").option("header", True).csv(str(output / "category_report"))
        product_report.write.mode("overwrite").parquet(str(output / "product_report"))
        print(f"Reports written to {output}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
