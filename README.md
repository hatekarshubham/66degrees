**ETL Pipeline using Apache Spark, Apache Beam, BigQuery, and Cloud Composer**

**Overview**
This repository contains an ETL pipeline that extracts, transforms, and loads data into Google BigQuery using Apache Spark, Apache Beam, and Cloud Composer (Apache Airflow) for orchestration.

**Pipeline Components**

1. Data Extraction
Data is extracted from various sources such as CSV, JSON, and Parquet files.
Apache Beam and Apache Spark are used to process and clean the raw data before loading it into BigQuery staging tables.

2. Data Transformation
SQL scripts in BigQuery are used to process and transform the data.
Data is structured into dimension tables and fact tables following a star schema.

3. Data Loading
The transformed data is loaded into BigQuery for analytics.
All transformations are performed using SQL scripts inside BigQuery.

4. Orchestration
Cloud Composer (Apache Airflow) is used to schedule and manage the workflow.
DAGs automate the entire ETL process, ensuring data consistency and job scheduling.
