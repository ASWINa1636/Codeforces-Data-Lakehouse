from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"


COMMON_ENV = {
    "PYTHONPATH": f"{PROJECT_DIR}/src",
    "POSTGRES_HOST": "postgres",
    "POSTGRES_PORT": "5432",
    "POSTGRES_DATABASE": "codeforces_dw",
    "POSTGRES_USER": "codeforces",
    "POSTGRES_PASSWORD": "codeforces_dev_password",
    "DBT_PROFILES_DIR": f"{PROJECT_DIR}/dbt",
}


with DAG(
    dag_id="codeforces_data_pipeline",
    description="End-to-end Codeforces data lakehouse pipeline",
    start_date=datetime(2026, 9, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["codeforces", "data-engineering", "lakehouse"],
) as dag:

    ingest_codeforces = BashOperator(
        task_id="ingest_codeforces",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/ingest_problemset.py"
        ),
        env=COMMON_ENV,
    )

    process_parquet = BashOperator(
        task_id="process_parquet",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/process_problemset.py"
        ),
        env=COMMON_ENV,
    )

    load_postgres = BashOperator(
        task_id="load_postgres",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/load_postgres.py"
        ),
        env=COMMON_ENV,
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "dbt build "
            "--project-dir dbt/codeforces_warehouse"
        ),
        env=COMMON_ENV,
    )

    validate_pipeline = BashOperator(
        task_id="validate_pipeline",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            "python scripts/validate_pipeline.py"
        ),
        env=COMMON_ENV,
    )

    (
        ingest_codeforces
        >> process_parquet
        >> load_postgres
        >> dbt_build
        >> validate_pipeline
    )
    