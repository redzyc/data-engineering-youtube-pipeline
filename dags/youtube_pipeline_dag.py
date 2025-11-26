from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

SPARK_MASTER = "spark://spark-master:7077"
SPARK_CONTAINER = "spark-master"

JARS = "/opt/spark/jars-custom/hadoop-aws-3.3.4.jar,/opt/spark/jars-custom/aws-java-sdk-bundle-1.12.540.jar,/opt/spark/jars-custom/postgresql-42.7.8.jar"

SCRIPT_SILVER = "/opt/spark/jobs/process_raw_to_silver.py"
SCRIPT_GOLD = "/opt/spark/jobs/process_silver_to_gold.py"

cmd_silver = f"/usr/local/bin/docker exec {SPARK_CONTAINER} /opt/spark/bin/spark-submit --master {SPARK_MASTER} --jars {JARS} {SCRIPT_SILVER}"
cmd_gold = f"/usr/local/bin/docker exec {SPARK_CONTAINER} /opt/spark/bin/spark-submit --master {SPARK_MASTER} --jars {JARS} {SCRIPT_GOLD}"

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='youtube_pipeline_dag',
    default_args=default_args,
    description='End-to-end batch pipeline for YouTube data',
    schedule_interval='0 12 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'docker','youtube']
) as dag:

    process_raw_to_silver = BashOperator(
        task_id='process_raw_to_silver',
        bash_command=cmd_silver,
    )

    process_silver_to_gold = BashOperator(
        task_id='process_silver_to_gold',
        bash_command=cmd_gold,
    )

    process_raw_to_silver >> process_silver_to_gold