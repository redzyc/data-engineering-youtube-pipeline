CREATE USER airflow WITH PASSWORD 'airflow';
CREATE DATABASE airflow OWNER airflow;
GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;

CREATE DATABASE superset_db;


\c youtube_analytics;
CREATE SCHEMA IF NOT EXISTS speed_layer;
CREATE SCHEMA IF NOT EXISTS gold_layer;

CREATE TABLE IF NOT EXISTS speed_layer.realtime_stats(
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    channel_title VARCHAR(255),
    total_views BIGINT,
    video_count INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS gold_layer.channel_daily_stats (
    channel_title VARCHAR(255),
    total_views BIGINT,
    avg_likes DOUBLE PRECISION,
    report_date DATE
);

GRANT ALL PRIVILEGES ON SCHEMA speed_layer TO PUBLIC;
GRANT ALL PRIVILEGES ON SCHEMA gold_layer TO PUBLIC;
