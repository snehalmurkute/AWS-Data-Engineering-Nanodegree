import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = ("""CREATE TABLE staging_events (
    artist TEXT,
    auth TEXT,
    firstName TEXT,
    gender CHAR(1),
    itemInSession INT,
    lastName TEXT,
    length FLOAT,
    level VARCHAR(4),
    location TEXT,
    method VARCHAR(6),
    page VARCHAR(24),
    registration BIGINT,
    sessionId INT,
    song TEXT,
    status INT,
    ts BIGINT,
    userAgent TEXT,
    userId INT
 )
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs (
    artist_id        VARCHAR(18),
    artist_latitude  FLOAT,
    artist_location  VARCHAR(500),
    artist_longitude FLOAT,
    artist_name      VARCHAR(500),
    duration         FLOAT,
    num_songs        INTEGER,
    song_id          VARCHAR(18),
    title            VARCHAR(500),
    year             INTEGER)
""")

songplay_table_create = ("""CREATE TABLE songplays (
    songplay_id INT IDENTITY(0,1) NOT NULL,
    start_time TIMESTAMP,
    user_id INT,
    level VARCHAR(25),
    song_id VARCHAR(25),
    artist_id VARCHAR(25),
    session_id INT,
    location TEXT,
    user_agent TEXT)
""")

user_table_create = ("""CREATE TABLE users (
    user_id INT ,
    first_name TEXT,
    last_name TEXT,
    gender CHAR(4),
    level VARCHAR(25)
  )
""")

song_table_create = ("""CREATE TABLE songs (
    song_id VARCHAR(18),
    title VARCHAR(500),
    artist_id VARCHAR(18),
    year INT ,
    duration FLOAT
  )
""")

artist_table_create = ("""CREATE TABLE artists (
    artist_id VARCHAR(18),
    name VARCHAR(500),
    location VARCHAR(500),
    latitude FLOAT,
    longitude FLOAT
  )
""")

time_table_create = ("""CREATE TABLE time (
    start_time TIMESTAMP,
    hour SMALLINT,
    day SMALLINT,
    week SMALLINT,
    month SMALLINT ,
    year SMALLINT,
    weekday SMALLINT
  )
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events
from '{}'
iam_role '{}'
FORMAT AS JSON '{}'
region 'us-west-2'
""").format(
    config.get("S3", "LOG_DATA"),
    config.get("IAM_ROLE", "ARN"),
    config.get("S3", "LOG_JSONPATH"))

staging_songs_copy = ("""copy staging_songs 
from '{}' 
iam_role '{}'
FORMAT AS JSON 'auto'
region 'us-west-2'
""").format(config.get("S3", "SONG_DATA"),
            config.get("IAM_ROLE", "ARN"))

# FINAL TABLES

songplay_table_insert = (""" INSERT INTO songplays (start_time,
    user_id,
    level,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent)
SELECT  TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 second' AS start_time, e.userid, e.level, s.song_id, s.artist_id, e.sessionid, e.location, e.useragent
FROM staging_songs s LEFT JOIN staging_events e
ON s.title = e.song
Where e.page = 'NextSong'
""")

user_table_insert = ("""INSERT INTO users(user_id, first_name, last_name, gender, level)
WITH uniq_staging_events AS (
	SELECT userid, firstName, lastName, gender, level,
		   ROW_NUMBER() OVER(PARTITION BY userid ORDER BY ts DESC) AS rank
	FROM staging_events
            WHERE userid IS NOT NULL
)
SELECT userid, firstName, lastName, gender, level
	FROM uniq_staging_events
WHERE rank = 1""")

song_table_insert = (""" INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT distinct song_id, title, artist_id, year, duration
FROM staging_songs
""")

artist_table_insert = (""" INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT distinct artist_id, artist_name, artist_location, artist_latitude, artist_longitude
FROM staging_songs
""")

time_table_insert = (""" INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT  distinct start_time,
EXTRACT(hour FROM start_time) AS hour,
EXTRACT(day FROM start_time) AS day,
EXTRACT(week FROM start_time) AS week,
EXTRACT(month FROM start_time) AS month,
EXTRACT(year FROM start_time) AS year,
EXTRACT(weekday FROM start_time) AS weekday
FROM songplays
""")

# QUERY LISTS


create_table_queries = [staging_events_table_create, staging_songs_table_create,songplay_table_create,
                        user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop,
                     song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert,
                        time_table_insert]
