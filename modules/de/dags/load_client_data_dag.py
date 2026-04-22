# Airflow DAG that loads the raw customer source files.

import pendulum
from airflow.decorators import dag, task

from de_pipeline.etl import CustomerDataETL


@dag(
    dag_id="load_client_data",
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["de"],
)
def load_client_data_dag():
    """Expose the one-off customer ingestion workflow in Airflow."""

    @task
    def load_customer_file(source_key: str) -> None:
        CustomerDataETL().load_source_file(source_key)

    load_customer_file.override(task_id="load_customer_profiles")(
        "customer_profiles.csv"
    )
    load_customer_file.override(task_id="load_customer_activity")(
        "customer_activity.csv"
    )
    load_customer_file.override(task_id="load_labels")("labels.csv")


load_client_data = load_client_data_dag()
