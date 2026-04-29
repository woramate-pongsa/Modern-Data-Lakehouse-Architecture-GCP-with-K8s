import os
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from datetime import datetime, timedelta

# These would typically be provided by Airflow Variables or Env Vars
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "my-project-lakehouse-k8s")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'lakehouse_medallion_pipeline',
    default_args=default_args,
    description='Orchestrate Bronze to Gold processing via Spark Operator',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Bronze to Silver
    submit_bronze_to_silver = SparkKubernetesOperator(
        task_id='submit_bronze_to_silver',
        namespace="default",
        application_file="spark-app-bronze-silver.yaml", # This file needs to be available to Airflow
        do_xcom_push=True,
    )

    sensor_bronze_to_silver = SparkKubernetesSensor(
        task_id='sensor_bronze_to_silver',
        namespace="default",
        application_name="{{ task_instance.xcom_pull(task_ids='submit_bronze_to_silver')['metadata']['name'] }}",
        poke_interval=30,
    )

    # Task 2: Silver to Gold
    submit_silver_to_gold = SparkKubernetesOperator(
        task_id='submit_silver_to_gold',
        namespace="default",
        application_file="spark-app-silver-gold.yaml",
        do_xcom_push=True,
    )

    sensor_silver_to_gold = SparkKubernetesSensor(
        task_id='sensor_silver_to_gold',
        namespace="default",
        application_name="{{ task_instance.xcom_pull(task_ids='submit_silver_to_gold')['metadata']['name'] }}",
        poke_interval=30,
    )

    submit_bronze_to_silver >> sensor_bronze_to_silver >> submit_silver_to_gold >> sensor_silver_to_gold
