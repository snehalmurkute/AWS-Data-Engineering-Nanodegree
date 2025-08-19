# Sparkify ETL Data Pipeline with Apache Airflow

## 📌 Project Overview

A music streaming company Sparkify wants to automate and monitor their ETL pipelines to process data from S3 into Amazon Redshift.
This project implements a production-grade data pipeline using Apache Airflow with custom operators for:

    - Staging raw JSON data from S3 into Redshift.
    - Transforming and loading fact & dimension tables.
    - Running automated data quality checks.

The pipeline is dynamic, reusable, supports backfills, and ensures data integrity through monitoring and testing.

## 🛠️ Tech Stack

    - Apache Airflow – DAG orchestration
    - Amazon Redshift – Cloud data warehouse
    - Amazon S3 – Data lake (source)
    - AWS IAM – Access & security
    - Python – Custom operators & hooks
    - SQL – Data transformations & quality checks

## 🚀 Pipeline Workflow

    1. Begin Execution
    2. Stage Events & Songs Data (from S3 → Redshift staging tables)
    3. Load Fact Table → songplays
    4. Load Dimension Tables → users, songs, artists, time
    5. Run Data Quality Checks
    6. Stop Execution

## DAG Graph View
<img width="1180" height="432" alt="image" src="https://github.com/user-attachments/assets/bf6e65f3-e957-416f-ab90-0f48772367a2" />

## ⚙️ Key Features
🔹 Stage Operator

    - Loads JSON data from S3 to Redshift using COPY command
    - Supports templated S3 keys for timestamp-based backfills
    - Configurable for multiple sources

🔹 Fact & Dimension Operators

    - Reusable operators for inserting into fact/dim tables
    - Fact Table: Append-only
    - Dimension Tables: Configurable load mode (truncate-insert or append)

🔹 Data Quality Operator

    - Runs custom SQL test cases
    - Validates data completeness & consistency
    - Raises exceptions if tests fail

## 📊 Example Data Quality Checks

    - Ensure tables are not empty after load
    - Validate songplays.playid has no NULLs
    - Check row counts match expectations

## 📑 Datasets

    - Log Data: s3://udacity-dend/log_data (user activity logs)
    - Song Data: s3://udacity-dend/song-data (song metadata)

## 🔧 Setup Instructions

1. Prerequisites
    - AWS Account (S3, Redshift, IAM configured)
    - Airflow installed (local or Udacity workspace)
2. Steps
    - Create IAM User with S3 + Redshift access
    - Set up Redshift Serverless workgroup
3. Copy datasets from Udacity’s S3 bucket to my own
    - aws s3 cp s3://udacity-dend/log-data/ s3://<your-bucket>/log-data/ --recursive
    - aws s3 cp s3://udacity-dend/song-data/ s3://<your-bucket>/song-data/ --recursive
4. Configure Airflow Connections:
    - aws_credentials → IAM keys
    - redshift → Redshift cluster connection
5. Trigger DAG from Airflow UI

## ✅ Deliverables

    - Dynamic Airflow DAG with 9 tasks
    - Custom operators for staging, loading, and quality checks
    - Fully automated ETL pipeline with monitoring & error handling

## 📌 Learnings & Highlights

    - Built scalable, reusable Airflow operators
    - Gained hands-on experience with Redshift COPY, ETL workflows, and S3 integration
    - Implemented data quality frameworks to ensure reliable analytics-ready data

