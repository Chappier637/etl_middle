from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pymongo import MongoClient
import pandas as pd

# Настройки DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Создание DAG
dag = DAG(
    "mongo_to_postgres",
    default_args=default_args,
    description="DAG to transfer data from MongoDB to PostgreSQL",
    schedule_interval="@daily",  # Запускать ежедневно
    catchup=False,
)

# Функция для выгрузки данных из MongoDB
def extract_data_from_mongo():
    client = MongoClient("mongodb://root:example@mongodb:27017/")
    db = client.social_media

    users = list(db.users.find({}, {"_id": 0}))
    posts = list(db.posts.find({}, {"_id": 0}))
    comments = list(db.comments.find({}, {"_id": 0}))
    likes = list(db.likes.find({}, {"_id": 0}))
    follows = list(db.follows.find({}, {"_id": 0}))
    messages = list(db.messages.find({}, {"_id": 0}))
    communities = list(db.communities.find({}, {"_id": 0}))

    return {
        "users": users,
        "posts": posts,
        "comments": comments,
        "likes": likes,
        "follows": follows,
        "messages": messages,
        "communities": communities,
    }

# Функция для загрузки данных в PostgreSQL
def load_data_to_postgres(**kwargs):
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract_data_from_mongo")

    postgres_hook = PostgresHook(postgres_conn_id="pg")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    def insert_data(table_name, records):
        if not records:
            return
        columns = records[0].keys()
        columns_str = ", ".join(columns)
        values_placeholder = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_placeholder})"
        cursor.executemany(query, [tuple(record.values()) for record in records])
        conn.commit()

    insert_data("users", data["users"])
    insert_data("posts", data["posts"])
    insert_data("comments", data["comments"])
    insert_data("likes", data["likes"])
    insert_data("follows", data["follows"])
    insert_data("messages", data["messages"])
    insert_data("communities", data["communities"])

    cursor.close()
    conn.close()

extract_task = PythonOperator(
    task_id="extract_data_from_mongo",
    python_callable=extract_data_from_mongo,
    dag=dag,
)

load_task = PythonOperator(
    task_id="load_data_to_postgres",
    python_callable=load_data_to_postgres,
    provide_context=True,
    dag=dag,
)

extract_task >> load_task