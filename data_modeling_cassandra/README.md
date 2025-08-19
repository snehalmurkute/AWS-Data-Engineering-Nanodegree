# Data Modeling with Apache Cassandra – Sparkify

## 📌 Project Overview  
A startup called **Sparkify** wants to analyze songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, the data is stored in multiple CSV files, making it difficult to query.  

As the data engineer, I built a **Cassandra database** and designed an **ETL pipeline** in Python to:  
- Process raw event log CSV files  
- Model denormalized tables in Apache Cassandra  
- Insert and query data to answer specific business questions  

This project demonstrates **NoSQL data modeling**, **ETL pipeline design**, and **query optimization** for analytics.  

---

## 📂 Dataset  
The event log data is stored in CSV files partitioned by date under the directory `event_data/`.  

Example files:  
- `event_data/2018-11-08-events.csv`  
- `event_data/2018-11-09-events.csv`  

A new consolidated CSV file `event_datafile_new.csv` is created during preprocessing for easier ingestion into Cassandra.  

---

## ⚙️ Project Steps  

### 1. Data Preprocessing  
- Iterated over all raw event files in `event_data/`  
- Extracted key fields (artist, song, length, sessionId, userId, etc.)  
- Generated a single clean file `event_datafile_new.csv`  

### 2. Data Modeling with Cassandra  
Designed denormalized tables based on the analytics team’s queries.  

#### Example Queries & Data Model  

1. **Query 1** – Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession  = 4.  
   ```sql
   CREATE TABLE IF NOT EXISTS song_session_history (
       session_id int,
       item_in_session int,
       artist text,
       song text,
       length float,
       PRIMARY KEY (session_id, item_in_session)
   );
   ```  

2. **Query 2** – Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182. 
   ```sql
   CREATE TABLE IF NOT EXISTS user_session_history (
       user_id int,
       session_id int,
       item_in_session int,
       artist text,
       song text,
       first_name text,
       last_name text,
       PRIMARY KEY ((user_id, session_id), item_in_session)
   );
   ```  

3. **Query 3** – Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'.  
   ```sql
   CREATE TABLE IF NOT EXISTS song_listeners (
       song text,
       user_id int,
       first_name text,
       last_name text,
       PRIMARY KEY (song, user_id)
   );
   ```  

### 3. ETL Pipeline  
- Wrote Python scripts to:  
  - Drop & create Cassandra tables  
  - Insert records from `event_datafile_new.csv`  
  - Run SELECT queries to verify data  

---

## 📊 Tech Stack  
- **Python** (pandas, csv, cassandra-driver)  
- **Apache Cassandra** (NoSQL database)  
- **Jupyter Notebook**  

---

## ✅ Key Learnings  
- Applied **NoSQL data modeling** concepts (denormalization, partitioning, clustering keys)  
- Designed tables based on **query-driven schema design**  
- Built an **ETL pipeline in Python** to process CSV data  
- Gained hands-on experience with **Apache Cassandra query optimization**  

---
## 📈 Sample Query Results  

**Query 1** – Give me the artist, song title and song's length in the music app history that was heard during sessionId = 338, and itemInSession  = 4. 

| Artist    | Song Title                      | Length (seconds)   |
| --------- | ------------------------------- | ------------------ |
| Faithless | Music Matters (Mark Knight Dub) | 495.30731201171875 |


**Query 2** – Give me only the following: name of artist, song (sorted by itemInSession) and user (first and last name) for userid = 10, sessionid = 182.

| Artist            | Song                                                 | User        |
| ----------------- | ---------------------------------------------------- | ----------- |
| Down To The Bone  | Keep On Keepin' On                                   | Sylvie Cruz |
| Three Drives      | Greece 2000                                          | Sylvie Cruz |
| Sebastien Tellier | Kilometer                                            | Sylvie Cruz |
| Lonnie Gordon     | Catch You Baby (Steve Pitron & Max Sanna Radio Edit) | Sylvie Cruz |


**Query 3** – Give me every user name (first and last) in my music app history who listened to the song 'All Hands Against His Own'. 

| First Name | Last Name |
| ---------- | --------- |
| Jacqueline | Lynch     |
| Tegan      | Levine    |
| Sara       | Johnson   |
