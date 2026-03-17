from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id="pipeline_gps",
    default_args=default_args,
    description="Procesamiento de datos GPS con Spark",
    schedule_interval="*/5 * * * *",
    catchup=False,
    tags=['gps', 'spark'],
) as dag:

    process_spark = BashOperator(
        task_id="process_gps_data",
        bash_command="python /opt/airflow/spark/spark_processor.py",
        env={
            'DB_HOST': 'postgres-postgis',
            'DB_USER': 'admin',
            'DB_PASSWORD': 'admin',
            'DB_NAME': 'monitoreo'
        }
    )

    store = BashOperator(
        task_id="task_store",
        bash_command="echo 'Datos almacenados en PostgreSQL'"
    )

    dashboard = BashOperator(
        task_id="task_dashboard",
        bash_command="echo 'Dashboard actualizado'"
    )

    process_spark >> store >> dashboard
