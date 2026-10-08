from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, current_timestamp, split, to_timestamp, trim


BASE_DIR = Path(__file__).parent


def main():
    input_path = BASE_DIR / "input_logs"
    checkpoint = BASE_DIR / "checkpoints" / "log_metrics"
    spark = SparkSession.builder.appName("RealtimeLogAnalysis").master("local[*]").getOrCreate()
    try:
        source = spark.readStream.text(str(input_path))
        parts = split(col("value"), "\\|", 4)
        events = source.select(to_timestamp(trim(parts.getItem(0)), "yyyy-MM-dd HH:mm:ss").alias("event_time"), trim(parts.getItem(1)).alias("level"), trim(parts.getItem(2)).alias("service"), trim(parts.getItem(3)).alias("message")).filter(col("event_time").isNotNull() & col("level").isin("INFO", "WARNING", "ERROR", "DEBUG"))
        metrics = events.groupBy("level", "service").agg(count("*").alias("event_count")).withColumn("processed_at", current_timestamp())
        query = metrics.writeStream.outputMode("complete").format("console").option("truncate", False).option("checkpointLocation", str(checkpoint)).start()
        print(f"Watching {input_path}. Add new text files, then press Ctrl+C to stop.")
        query.awaitTermination()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
