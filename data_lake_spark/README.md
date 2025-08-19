# STEDI Human Balance Analytics – Data Lakehouse Project

## 📌 Project Overview

This project simulates a real-world data engineering pipeline for STEDI, a company developing a Step Trainer IoT device and mobile app that helps users practice balance exercises. The goal is to:

    - Collect IoT sensor data and mobile accelerometer data
    - Curate the data into a Data Lakehouse using AWS Glue + Spark
    - Build trusted and curated zones in Amazon S3
    - Prepare a machine learning–ready dataset for the Data Science team

The final curated dataset will allow data scientists to train a model that accurately detects steps in real time.

## 🏗️ Architecture

                ┌───────────────────────────────┐
                │        Data Sources           │
                │ ─ customer_landing (website)  │
                │ ─ accelerometer_landing (app) │
                │ ─ step_trainer_landing (IoT)  │
                └───────────────┬───────────────┘
                                │
                        AWS S3 Landing Zone
                                │
                ┌───────────────▼───────────────┐
                │       AWS Glue + Spark        │
                │   • Data cleaning & joins     │
                │   • Trusted & Curated zones   │
                └───────────────┬───────────────┘
                                │
                        AWS S3 Lakehouse
                                │
                ┌───────────────▼───────────────┐
                │        AWS Athena Queries     │
                │   • SQL queries on curated    │
                │   • Verification & analytics  │
                └───────────────────────────────┘

## 📂 Data Zones

   1. Landing Zone (Raw Data)
        - customer_landing – customer records (opt-in for research flag included)
        - accelerometer_landing – mobile app accelerometer readings
        - step_trainer_landing – IoT device step trainer readings

   2. Trusted Zone (Filtered Data)
        - customer_trusted – only customers who consented to share data
        - accelerometer_trusted – accelerometer records from consenting customers
        - step_trainer_trusted – step trainer records linked to valid customers

   3. Curated Zone (Final Data Lakehouse)
        customers_curated – customers with both accelerometer + consent
        machine_learning_curated – combined accelerometer + step trainer data (ML-ready)

## ⚙️ Pipeline Steps

    1. Create Landing Zone Tables (Athena + Glue Catalog)
        - customer_landing.sql
        - accelerometer_landing.sql
        - step_trainer_landing.sql

    2. Build Trusted Zone
        - Glue Job: customer_landing ➝ customer_trusted
        - Glue Job: accelerometer_landing ➝ accelerometer_trusted
        - Validate with Athena queries

    3. Fix Customer Serial Number Issue
        Create customers_curated by joining customer_trusted + accelerometer_trusted

    4. Step Trainer Data Integration
        Glue Job: step_trainer_landing ➝ step_trainer_trusted (only valid customers)

    5. Final Machine Learning Dataset
        - Glue Job: accelerometer_trusted + step_trainer_trusted ➝ machine_learning_curated
        - Joins accelerometer & step trainer readings by timestamp

## 📑 Deliverables

    1. SQL Scripts (in /scripts)
        - customer_landing.sql
        - accelerometer_landing.sql
        - step_trainer_landing.sql

    2. AWS Glue Jobs (in /glue_jobs)
        - customer_trusted.py
        - accelerometer_trusted.py
        - customers_curated.py
        - step_trainer_trusted.py
        - machine_learning_curated.py

    3. Athena Query Screenshots (in /screenshots)
        - customer_landing.png
        - accelerometer_landing.png
        - step_trainer_landing.png
        - customer_trusted.png
        - customers_curated.png

## 🛠️ Technologies Used

    - Python + PySpark – data transformations
    - AWS Glue – ETL jobs
    - Amazon S3 – Data Lake storage
    - AWS Athena – SQL queries
    - AWS Glue Catalog – schema management

## 🚀 How to Run This Project

    1. Upload datasets to S3 Landing Zone buckets:
        - s3://<bucket>/customer_landing/
        - s3://<bucket>/accelerometer_landing/
        - s3://<bucket>/step_trainer_landing/

    2. Run Glue Jobs in order:
        Customer Trusted → Accelerometer Trusted → Customers Curated → Step Trainer Trusted → Machine Learning Curated

    3. Query with Athena to validate transformations
    
## ✅ Outcome
With this project, I demonstrated my ability to design and implement a scalable AWS Data Lakehouse pipeline for IoT + mobile sensor data using Spark + AWS Glue + Athena.

