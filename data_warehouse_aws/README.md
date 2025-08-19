# 🎶 Data Warehouse on AWS (Sparkify ETL)

## 📌 Introduction
Sparkify, a fast-growing music streaming startup, has expanded its user base and song catalog. To support data-driven insights, Sparkify needs a cloud-based **data warehouse solution** for scalable analytics.  

As the Data Engineer, I designed and implemented an **ETL pipeline** to extract data from **AWS S3**, stage it in **Amazon Redshift**, and transform it into a **star schema** optimized for analytical queries. This enables the analytics team to gain insights into user behavior and song play trends.

---

## 🏗️ System Architecture
**Source → Staging → Analytics**

<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/53a9206b-20b4-47c6-8eba-f961fb3c13ea" />

1. **S3**: Raw JSON logs (user activity) & JSON metadata (songs)  
2. **Amazon Redshift**: Cloud Data Warehouse to stage and transform data  
3. **ETL Pipeline**: Python scripts to automate extraction, loading, and transformation  
4. **Star Schema**: Fact & dimension tables optimized for queries  

---

## 📂 Datasets
- **Song Data**: `s3://udacity-dend/song_data`  
   - Subset of the Million Song Dataset (JSON format).  
   - Contains metadata about songs and artists.  

- **Log Data**: `s3://udacity-dend/log_data`  
   - JSON event logs from Sparkify’s music app.  
   - Includes user activity like song plays, session info, and device data.  

- **Log JSON Metadata**: `s3://udacity-dend/log_json_path.json`  
   - Defines the schema for parsing JSON logs into Redshift.  

---

## ⭐ Schema Design (Star Schema)
To optimize queries for **song play analysis**, a **star schema** was implemented.  

**Fact Table**  
- **songplays** → Records of each song play (joins logs with song metadata)  

**Dimension Tables**  
- **users** → App users (user_id, name, gender, level)  
- **songs** → Song details (song_id, title, artist_id, year, duration)  
- **artists** → Artist details (artist_id, name, location, latitude, longitude)  
- **time** → Timestamps broken into hour, day, week, month, year, weekday  

---

## 🚀 Project Workflow
### 1. Create Table Schemas
- Defined **DROP & CREATE statements** for staging, fact, and dimension tables.  
- Script: `create_tables.py`  

### 2. Build ETL Pipeline
- Extract data from **S3** → Load into **staging tables** on Redshift.  
- Transform staging data → Load into **fact & dimension tables**.  
- Script: `etl.py`  

### 3. AWS Setup
- Launched **Amazon Redshift cluster**.  
- Created **IAM Role** with S3 read permissions.  
- Configured cluster & connection info in `dwh.cfg`.  

### 4. Testing & Validation
- Ran `create_tables.py` → Verified schema in Redshift Query Editor.  
- Ran `etl.py` → Loaded data and validated with analytical queries.  
- Example Query: Top 10 most popular songs.  

---

## 🧰 Tools & Technologies

 - **AWS S3** → Data Lake
 - **Amazon Redshift** → Cloud Data Warehouse
 - **Python (psycopg2, configparser)** → ETL Pipeline
 - **SQL** → Schema Design & Data Transformations

## ⚙️ Project Structure
```bash
├── create_tables.py     # Creates fact & dimension tables in Redshift
├── etl.py               # ETL pipeline: Load data from S3 → Redshift → Star Schema
├── sql_queries.py       # SQL statements for schema & ETL
├── dwh.cfg              # Config file with Redshift & IAM role details
└── README.md            # Project documentation
```
## 📊 Example Queries
###  **1. Most Played Song**

`SELECT s.title, COUNT(*) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY play_count DESC
LIMIT 1;`

### **2. Busiest Hour of the Day**

`SELECT t.hour, COUNT(*) AS total_plays
FROM songplays sp
JOIN time t ON sp.start_time = t.start_time
GROUP BY t.hour
ORDER BY total_plays DESC
LIMIT 1;`

### **3. Most Active Users**

`SELECT u.user_id, u.first_name, u.last_name, COUNT(*) AS songplays
FROM songplays sp
JOIN users u ON sp.user_id = u.user_id
GROUP BY u.user_id, u.first_name, u.last_name
ORDER BY songplays DESC
LIMIT 5;`

### **4. Top Artists by Play Count**

`SELECT a.name AS artist_name, COUNT(*) AS play_count
FROM songplays sp
JOIN artists a ON sp.artist_id = a.artist_id
GROUP BY a.name
ORDER BY play_count DESC
LIMIT 5;`

## ✅ Key Takeaways

 - Designed a scalable cloud-based data warehouse.
 - Automated data loading from S3 → Redshift.
 - Implemented a star schema optimized for analytics.
 - Enabled Sparkify’s analytics team to query insights on user activity and song plays.

## 🧑‍💻 How to Run

 1. Update dwh.cfg with Redshift cluster & IAM details.
 2. Run schema creation:
 ```bash
   python create_tables.py
 ```
 4. Run ETL pipeline:
 ```bash
    python etl.py
 ```
 5. Query results in AWS Redshift Query Editor.
