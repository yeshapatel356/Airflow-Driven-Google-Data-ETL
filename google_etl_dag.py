from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
from google_etl import run_google_etl
from analyze_reviews import analyze_positive_dishes 
import os

# Function to check if API key loads correctly
def check_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found in environment.")
    print(f"API Key loaded successfully: {api_key}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2024, 4, 6),
}

dag = DAG(
    'google_etl_dag',
    default_args=default_args,
    description='Run Google Place ETL queries',
    schedule_interval=timedelta(days=1),
    catchup=False,
)

check_key_task = PythonOperator(
    task_id='check_api_key',
    python_callable=check_api_key,
    dag=dag,
)

run_etl_task = PythonOperator(
    task_id='run_google_etl',
    python_callable=run_google_etl,
    dag=dag,
)

analyze_reviews_task = PythonOperator(
    task_id='analyze_reviews',
    python_callable=analyze_positive_dishes
)

# Define task sequence
run_etl_task >> analyze_reviews_task 

