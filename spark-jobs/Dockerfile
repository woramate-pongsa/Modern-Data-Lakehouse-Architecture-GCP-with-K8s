# Use an official Spark image as a parent image
FROM apache/spark-py:v3.4.0

USER root

# Set working directory
WORKDIR /app

# Install necessary libraries if any (pyspark is already in the image)
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Download Delta Lake JARs (using specific versions compatible with Spark 3.4.0)
# Download Delta Lake JARs (using specific versions compatible with Spark 3.4.0)
ENV DELTA_VERSION=2.4.0
ADD https://repo1.maven.org/maven2/io/delta/delta-core_2.12/${DELTA_VERSION}/delta-core_2.12-${DELTA_VERSION}.jar /opt/spark/jars/
ADD https://repo1.maven.org/maven2/io/delta/delta-storage/${DELTA_VERSION}/delta-storage-${DELTA_VERSION}.jar /opt/spark/jars/

# Download GCS Connector (Compatible with Hadoop 3.x)
ADD https://repo1.maven.org/maven2/com/google/cloud/bigdataoss/gcs-connector/hadoop3-2.2.23/gcs-connector-hadoop3-2.2.23-shaded.jar /opt/spark/jars/


# Copy the Spark jobs into the image
COPY bronze_to_silver.py .
COPY silver_to_gold.py .

