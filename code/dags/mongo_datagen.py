from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Путь к скрипту
SCRIPT_PATH = "/opt/airflow/dags/utils/data_generation.py"

# Функция для выполнения скрипта
def run_data_generation_script():
    try:
        result = subprocess.run(["python", SCRIPT_PATH], check=True, capture_output=True, text=True)
        print("Script output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Script failed with error:", e.stderr)
        raise e

# Аргументы DAG по умолчанию
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Создание DAG
dag = DAG(
    "generate_mongodb_data",
    default_args=default_args,
    description="DAG to generate social media data for MongoDB",
    schedule_interval="@daily",  # Запускать ежедневно
    catchup=False,
)

# Задача для генерации данных
generate_data_task = PythonOperator(
    task_id="generate_mongodb_data",
    python_callable=run_data_generation_script,
    dag=dag,
)

# Настройка порядка выполнения задач
generate_data_task