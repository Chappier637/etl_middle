from airflow import DAG
from airflow.operators.python import PythonOperator
from utils.default_args import DEFAULT_ARGS
from adapters.pg_adapter import PostgresAdapter


def pg_init_migration():
    pg_conn = PostgresAdapter()
    with open("/opt/airflow/sql/pg_migration.sql") as file:
        sql_query = file.read()
    rows = pg_conn.execute_commit_query(sql_query)

with DAG(
    dag_id="initial_migration",
    default_args=DEFAULT_ARGS,
    tags=["migration"],
) as dag:
        
        postgres_migrate = PythonOperator(
        task_id="postgres_migrate",
        python_callable=pg_init_migration,
        )
        
postgres_migrate
