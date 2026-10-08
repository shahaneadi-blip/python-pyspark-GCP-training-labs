import os
from pathlib import Path

from pyspark.sql import SparkSession


BASE_DIR = Path(__file__).parent


def required(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Set environment variable {name} before running this lab.")
    return value


def main():
    spark = SparkSession.builder.appName("JdbcExtractExport").master("local[*]").getOrCreate()
    try:
        url = required("JDBC_URL")
        table = required("JDBC_TABLE")
        properties = {"user": required("JDBC_USER"), "password": required("JDBC_PASSWORD"), "driver": os.getenv("JDBC_DRIVER", "com.microsoft.sqlserver.jdbc.SQLServerDriver")}
        source = spark.read.jdbc(url=url, table=table, properties=properties)
        source.show(10, truncate=False)
        output = BASE_DIR / "output" / "jdbc_extract_parquet"
        source.write.mode("overwrite").parquet(str(output))
        print(f"Exported {source.count()} rows to {output}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
