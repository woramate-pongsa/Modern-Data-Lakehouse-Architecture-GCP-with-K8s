import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, window

# Initialize Spark Session with Delta support
spark = SparkSession.builder \
    .appName("Silver to Gold") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

# Configuration from environment variables
SILVER_BUCKET = os.getenv("SILVER_BUCKET", "my-project-lakehouse-k8s-lake-silver")
GOLD_BUCKET = os.getenv("GOLD_BUCKET", "my-project-lakehouse-k8s-lake-gold")

SILVER_PATH = f"gs://{SILVER_BUCKET}/events/"
GOLD_PATH = f"gs://{GOLD_BUCKET}/user_event_summary/"

def main():
    print(f"Reading data from {SILVER_PATH} in Delta format...")
    
    # Read Silver Delta data
    df_silver = spark.read.format("delta").load(SILVER_PATH)
    
    # Aggregate: User-level event summary
    df_gold = df_silver.groupBy("user_id", "event_type") \
        .agg(count("*").alias("event_count")) \
        .orderBy("user_id", "event_type")
    
    print(f"Writing aggregated data to {GOLD_PATH} in Delta format...")
    
    # Save to Gold layer in Delta format
    df_gold.write.format("delta").mode("overwrite").save(GOLD_PATH)
    
    print("Done. Gold layer updated in Delta format.")

if __name__ == "__main__":
    main()
