import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator, ShortCircuitOperator

sys.path.append(str(Path(__file__).parents[1]))

from src.extract import extract_data  # noqa
from src.load import load_data  # noqa
from src.prepare_report import prepare_report  # noqa
from src.transform import transform_data  # noqa


def is_content_filled(**kwargs):
    # Pull the HTML content from the previous task
    html_content = kwargs["ti"].xcom_pull(task_ids="prepare_email_content")
    # Check if the content is not None and not empty
    return html_content is not None and html_content.strip() != ""


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 31),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "housing_dag",
    default_args=default_args,
    description="EZ housing DAG",
    schedule_interval="4 8,11,14,17,19 * * 1-6",
    catchup=False,
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

prepare_email_content = PythonOperator(
    task_id="prepare_email_content",
    python_callable=prepare_report,
    dag=dag,
    provide_context=True,
)

check_content_task = ShortCircuitOperator(
    task_id="check_html_content_is_filled",
    python_callable=is_content_filled,
    provide_context=True,
    dag=dag,
)

send_email = EmailOperator(
    task_id="send_report_email",
    to=os.getenv("EMAIL"),
    subject="Housing Report",
    html_content="{{ ti.xcom_pull(task_ids='prepare_email_content') }}",
    dag=dag,
)

# Define task dependencies in a multiline format
extract_task >> transform_task
transform_task >> load_task
load_task >> prepare_email_content
prepare_email_content >> check_content_task
check_content_task >> send_email
