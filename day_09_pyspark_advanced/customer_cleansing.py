from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, initcap, lower, regexp_replace, trim, when


BASE_DIR = Path(__file__).parent


def main():
    spark = SparkSession.builder.appName("CustomerCleansing").master("local[*]").getOrCreate()
    try:
        customers = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "customers.csv"))
        cleaned = (
            customers
            .withColumn("customer_id", trim(col("customer_id")))
            .withColumn("customer_name", initcap(trim(col("customer_name"))))
            .withColumn("email", lower(trim(col("email"))))
            .withColumn("phone", regexp_replace(trim(col("phone")), "[^0-9]", ""))
            .withColumn("city", initcap(trim(col("city"))))
            .withColumn("age", when(col("age").between(18, 100), col("age")).otherwise(None))
            .na.fill({"city": "Unknown", "age": 0})
            .filter(col("customer_id").isNotNull() & col("customer_name").isNotNull())
            .dropDuplicates(["customer_id"])
        )
        output = BASE_DIR / "output"
        cleaned.orderBy("customer_id").show(truncate=False)
        cleaned.write.mode("overwrite").option("header", True).csv(str(output / "cleaned_customers_csv"))
        cleaned.write.mode("overwrite").parquet(str(output / "cleaned_customers_parquet"))
        print(f"Input rows: {customers.count()}")
        print(f"Cleaned rows: {cleaned.count()}")
        print(f"Outputs: {output}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
