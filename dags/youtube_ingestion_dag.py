from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import os

INGESTION_SCRIPT_PATH = "/opt/airflow/ingestion_scripts/youtube_client.py"

cmd_ingest = f"""
    pip install --user --break-system-packages --no-cache-dir google-api-python-client python-dotenv && \
    python3 {INGESTION_SCRIPT_PATH}
"""
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='youtube_ingest_hourly',
    default_args=default_args,
    description='Ingestion information from API',
    schedule_interval='@hourly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['spark', 'docker','youtube']
) as dag:

    ingest_data = BashOperator(
        task_id='ingest_youtube_api',
        bash_command=cmd_ingest,
        env={'YOUTUBE_API_KEY': os.getenv('YOUTUBE_API_KEY', '')} 
    )