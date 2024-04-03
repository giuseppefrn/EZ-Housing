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


def check_task_output_filled(**kwargs):
    """
    General-purpose function to check if the
    output from specified tasks is not None and not empty.
    It iterates over the list of task IDs
    provided and checks each corresponding output.

    Args:
    **kwargs: containing 'task_ids', a list of task IDs to check,
              and 'ti', the task instance.

    Returns:
    bool: True if all specified tasks have outputs that are not None and not empty, False otherwise. # noqa
    """
    task_ids = kwargs.get("task_ids", [])
    ti = kwargs["ti"]

    for task_id in task_ids:
        task_output = ti.xcom_pull(task_ids=task_id)
        if not task_output or (
            isinstance(task_output, str) and task_output.strip() == ""
        ):
            return False
    return True


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
    provide_context=True,  # noqa
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

send_email = EmailOperator(
    task_id="send_report_email",
    to=os.getenv("EMAIL"),
    subject="Housing Report",
    html_content="{{ ti.xcom_pull(task_ids='prepare_email_content') }}",
    dag=dag,
)

check_extracted_task = ShortCircuitOperator(
    task_id="check_extracted_task",
    python_callable=check_task_output_filled,
    op_kwargs={"task_ids": ["extract"]},  # Specify the task_ids to check here
    provide_context=True,
    dag=dag,
)

check_email_filled_task = ShortCircuitOperator(
    task_id="check_content_filled",
    python_callable=check_task_output_filled,
    op_kwargs={
        "task_ids": ["prepare_email_content"]
    },  # Specify the task_ids to check here
    provide_context=True,
    dag=dag,
)


# Define task dependencies in a multiline format
extract_task >> check_extracted_task
check_extracted_task >> transform_task
transform_task >> load_task
load_task >> prepare_email_content
prepare_email_content >> check_email_filled_task
check_email_filled_task >> send_email
