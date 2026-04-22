# Airflow DAG that loads the previous month's sales data.

import pendulum
from airflow.decorators import dag, task

from de_pipeline.etl import SalesDataETL


@dag(
    dag_id="load_sales_data",
    schedule="0 0 1 * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["de"],
)
def load_sales_data_dag():
    """Schedule the monthly sales ingestion and aggregation flow."""

    @task(task_id="load_previous_month_sales")
    def load_previous_month_sales(**context) -> None:
        SalesDataETL().run(
            reference_datetime=context["logical_date"].in_timezone("UTC")
        )

    load_previous_month_sales()


load_sales_data = load_sales_data_dag()
