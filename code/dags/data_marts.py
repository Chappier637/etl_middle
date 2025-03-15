from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from utils.default_args import DEFAULT_ARGS

dag = DAG(
    dag_id=f'data_marts',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily',
    catchup=False
)

user_activity = SQLExecuteQueryOperator(
    task_id=f'user_activity',
    conn_id='pg',
    sql="./marts/user_activity.sql",
    autocommit=True,
    dag=dag
)

community_activity = SQLExecuteQueryOperator(
    task_id=f'community_activity',
    conn_id='pg',
    sql="./marts/community_activity.sql",
    autocommit=True,
    dag=dag
)

user_activity
community_activity