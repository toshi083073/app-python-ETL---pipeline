from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='sample_dag',
    default_args=default_args,
    description='A simple sample DAG',
    schedule_interval='@daily',
    start_date=datetime(2025, 5, 1),
    catchup=False,
    tags=['example'],
) as dag:

    task_hello = BashOperator(
        task_id='print_hello',
        bash_command='echo "Hello from Airflow!"'
    )

    task_hello
