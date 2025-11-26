CREATE DATABASE airflow_db;
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO de_user;

CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS analytics.channel_stats (
    channel_title VARCHAR(255),
    total_views BIGINT,
    avg_likes FLOAT,
    video_count INT,
    last_updated TIMESTAMP
);