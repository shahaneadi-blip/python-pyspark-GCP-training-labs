from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, col, concat_ws, count, lit, sum as spark_sum


def main():
    base_dir = Path(__file__).parent
    spark = SparkSession.builder.appName("EmployeeTransformations").master("local[*]").getOrCreate()
    try:
        employees = spark.read.option("header", True).option("inferSchema", True).csv(str(base_dir / "employees.csv"))
        renamed = employees.withColumnRenamed("name", "employee_name").withColumn("annual_salary", col("salary") * lit(12)).withColumn("employee_label", concat_ws(" - ", col("employee_name"), col("department")))
        print("Schema")
        renamed.printSchema()
        print("Employees with salary >= 50000")
        renamed.filter(col("salary") >= 50000).show(truncate=False)
        print("Department summary")
        renamed.groupBy("department").agg(count("employee_id").alias("employee_count"), spark_sum("salary").alias("monthly_salary"), avg("salary").alias("average_salary")).orderBy("department").show()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
