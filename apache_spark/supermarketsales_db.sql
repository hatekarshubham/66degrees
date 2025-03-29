-- Databricks notebook source
create database supermarketsales_db;

-- COMMAND ----------

CREATE or replace  TABLE supermarketsales_db.customer(
  customer_id BIGINT ,  
  customer_type string, 
  gender string,
  rating DOUBLE  
);

-- COMMAND ----------

CREATE or replace TABLE supermarketsales_db.product (
  product_id BIGINT ,  
  product_line string,  
  unit_price DOUBLE  
);

-- COMMAND ----------

CREATE or replace TABLE supermarketsales_db.sales_fact (
  invoice_id string, 
  customer_id BIGINT,
  product_id BIGINT,
  branch string,  
  city string,
  quantity integer,
  date date,
  time timestamp,  
  payment string,
  cogs DOUBLE,  
  tax DOUBLE,
  total DOUBLE,
  gross_income DOUBLE,
  gross_margin_percentage DOUBLE
);

-- COMMAND ----------

-- MAGIC %python
-- MAGIC dbutils.fs.rm("dbfs:/user/hive/warehouse/supermarketsales_db.db/product", recurse=True)
-- MAGIC