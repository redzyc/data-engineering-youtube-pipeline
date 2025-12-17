CREATE USER airflow WITH PASSWORD 'airflow';
CREATE DATABASE airflow OWNER airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

CREATE DATABASE superset_db;


\c youtube_analytics;
CREATE SCHEMA IF NOT EXISTS speed_layer;
CREATE SCHEMA IF NOT EXISTS gold_layer;


CREATE TABLE IF NOT EXISTS  speed_layer.realtime_stats(
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    video_id VARCHAR(50),       
    title TEXT,                  
    channel_title VARCHAR(255),
    total_views BIGINT,
    total_likes BIGINT,         
    total_comments BIGINT,    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
DROP TABLE IF EXISTS gold_layer.daily_stats;

CREATE TABLE gold_layer.daily_stats (
    video_id VARCHAR(50) PRIMARY KEY,
    title TEXT,
    channel_title VARCHAR(255),
    total_views BIGINT,
    total_likes BIGINT,
    total_comments BIGINT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

GRANT ALL PRIVILEGES ON SCHEMA speed_layer TO PUBLIC;
GRANT ALL PRIVILEGES ON SCHEMA gold_layer TO PUBLIC;
