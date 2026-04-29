-- 1. Create Dataset
CREATE SCHEMA IF NOT EXISTS `${PROJECT_ID}.analytics`
OPTIONS(location="asia-southeast1");

-- 2. Create External Table pointing to Gold Layer (Delta Lake)
CREATE OR REPLACE EXTERNAL TABLE `${PROJECT_ID}.analytics.user_event_summary`
OPTIONS (
  format = 'DELTA_LAKE',
  uris = ['gs://${PROJECT_ID}-lake-gold/user_event_summary/']
);

-- 3. Query Example
SELECT * FROM `${PROJECT_ID}.analytics.user_event_summary` LIMIT 10;

