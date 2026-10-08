from pathlib import Path
from time import perf_counter

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col, sum as spark_sum


BASE_DIR = Path(__file__).parent


def timed(label, action):
    started = perf_counter()
    result = action()
    print(f"{label}: {perf_counter() - started:.4f} seconds")
    return result


def main():
    spark = SparkSession.builder.appName("PerformanceComparison").master("local[*]").config("spark.sql.shuffle.partitions", "8").getOrCreate()
    try:
        sales = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "sales.csv"))
        products = spark.read.option("header", True).option("inferSchema", True).csv(str(BASE_DIR / "data" / "products.csv"))
        repeated_report = lambda frame: frame.groupBy("category").agg(spark_sum(col("quantity") * col("unit_price")).alias("revenue")).count()
        regular_join = sales.join(products, "product_id")
        timed("Regular join report", lambda: repeated_report(regular_join))
        broadcast_join = sales.join(broadcast(products), "product_id")
        timed("Broadcast join report", lambda: repeated_report(broadcast_join))
        cached = broadcast_join.repartition("category").cache()
        timed("Cached report first action", lambda: repeated_report(cached))
        timed("Cached report repeated action", lambda: repeated_report(cached))
        print(f"Input partitions: {sales.rdd.getNumPartitions()}")
        print(f"Optimized partitions: {cached.rdd.getNumPartitions()}")
        cached.unpersist()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
