from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import random
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'playing_dice',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['example playing dice'],
) as dag:

    def anhdd_play_function():
        print('Hi from python operator')

    def anhdd2_play_function():
        return random.randint(1, 6)

    anhdd_play = PythonOperator(
        task_id="python_task_1",  
        python_callable=anhdd_play_function,
    )

    anhdd2_play = PythonOperator(
        task_id="python_task_2", 
        python_callable=anhdd2_play_function,
    )
anhdd_play >> anhdd2_play