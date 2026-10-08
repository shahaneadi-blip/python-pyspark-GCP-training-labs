from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("FirstSparkSession").master("local[*]").getOrCreate()
    try:
        frame = spark.createDataFrame([(1, "Aarav"), (2, "Diya"), (3, "Rohan")], ["id", "name"])
        frame.show()
        print(f"Rows: {frame.count()}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
