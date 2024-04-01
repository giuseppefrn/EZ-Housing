import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append(str(Path(__file__).parents[1]))

from src.extract import extract_data  # noqa
from src.load import load_data  # noqa
from src.transform import transform_data  # noqa

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 31),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "catchup": False,
}

dag = DAG(
    "housing_dag",
    default_args=default_args,
    description="EZ housing DAG",
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract_data,
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform_data,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load_data,
    dag=dag,
)

extract_task >> transform_task >> load_task
