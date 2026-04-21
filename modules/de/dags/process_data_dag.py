# Airflow DAG that materializes the feature_store table.

import pendulum
from airflow.decorators import dag, task

from de_pipeline.etl import FeatureStoreETL


@dag(
    dag_id="process_data",
    schedule=None,
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    catchup=False,
    tags=["de"],
)
def process_data_dag():
    """Build the feature store after the raw customer tables are available."""

    @task(task_id="build_feature_store")
    def build_feature_store() -> None:
        FeatureStoreETL().run()

    build_feature_store()


process_data = process_data_dag()
