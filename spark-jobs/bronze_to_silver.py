import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Initialize Spark Session with Delta Lake support
spark = SparkSession.builder \
    .appName("Bronze to Silver") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Configuration from environment variables
BRONZE_BUCKET = os.getenv("BRONZE_BUCKET", "my-project-lakehouse-k8s-lake-bronze")
SILVER_BUCKET = os.getenv("SILVER_BUCKET", "my-project-lakehouse-k8s-lake-silver")

BRONZE_PATH = f"gs://{BRONZE_BUCKET}/*.json"
SILVER_PATH = f"gs://{SILVER_BUCKET}/events/"

# Define Schema (Matching Ingestion API)
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("event_type", StringType(), True),
    StructField("item_id", StringType(), True),
    StructField("timestamp", StringType(), True)
])

def main():
    print(f"Reading data from {BRONZE_PATH}...")
    
    # Read Bronze JSON data
    df_bronze = spark.read.json(BRONZE_PATH, schema=schema)
    
    # Transform: 
    # 1. Cast timestamp string to actual timestamp
    # 2. Add processing_timestamp
    # 3. Filter out rows where user_id is null OR timestamp casting failed (dirty data)
    df_silver = df_bronze \
        .withColumn("event_timestamp", col("timestamp").cast("timestamp")) \
        .withColumn("processing_timestamp", current_timestamp()) \
        .filter(col("user_id").isNotNull()) \
        .filter(col("event_timestamp").isNotNull()) \
        .drop("timestamp")
    
    # Deduplicate: Remove identical events within the same batch
    df_silver_clean = df_silver.dropDuplicates(["user_id", "event_type", "item_id", "event_timestamp"])
    
    print(f"Writing data to {SILVER_PATH} in Delta format...")
    
    # Save to Silver layer using Delta format
    df_silver_clean.write.format("delta").mode("append").save(SILVER_PATH)
    
    print("Done. Data cleaned, deduplicated, and saved to Delta Lake.")

if __name__ == "__main__":
    main()
