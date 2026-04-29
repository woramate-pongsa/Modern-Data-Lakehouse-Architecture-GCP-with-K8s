-- 1. Create Dataset
CREATE SCHEMA IF NOT EXISTS `my-project-lakehouse-k8s.analytics`
OPTIONS(location="asia-southeast1");

-- 2. Create External Table pointing to Gold Layer (Delta Lake)
CREATE OR REPLACE EXTERNAL TABLE `my-project-lakehouse-k8s.analytics.user_event_summary`
OPTIONS (
  format = 'DELTA_LAKE',
  uris = ['gs://my-project-lakehouse-k8s-lake-gold/user_event_summary/']
);

-- 3. Query Example
SELECT * FROM `my-project-lakehouse-k8s.analytics.user_event_summary` LIMIT 10;

