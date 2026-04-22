# Object-oriented ETL workflows used by the Airflow DAGs.

from datetime import datetime
from pathlib import Path

import pandas as pd

from de_pipeline.config import (
    CUSTOMER_SOURCE_FILES,
    STORES_SOURCE_FILE,
    sales_key_for_month,
)

from de_pipeline.database import PostgresWarehouse
from de_pipeline.storage import PublicS3Bucket
from de_pipeline.transformers import (
    build_feature_store_frame,
    build_monthly_sales_frame,
    resolve_previous_month_start,
)


class BaseETL:
    """Provide the shared dependencies needed by every ETL flow."""

    def __init__(
        self,
        warehouse: PostgresWarehouse | None = None,
        bucket: PublicS3Bucket | None = None,
    ) -> None:
        self.warehouse = warehouse or PostgresWarehouse()
        self.bucket = bucket or PublicS3Bucket()


class CustomerDataETL(BaseETL):
    """Load the customer source files into raw database tables."""

    def load_source_file(self, source_key: str) -> None:
        """Load one customer file into a same-name raw database table."""

        frame = self.bucket.fetch_csv(source_key)
        table_name = Path(source_key).stem
        self.warehouse.replace_table(table_name, frame)

    def run(self) -> None:
        for source_key in CUSTOMER_SOURCE_FILES:
            self.load_source_file(source_key)


class SalesDataETL(BaseETL):
    """Load one month of sales data and compute the matching monthly aggregate."""

    def run(self, reference_datetime: datetime | None = None) -> None:
        sale_month = resolve_previous_month_start(reference_datetime)
        print(f"Loading sales inputs for {sale_month.isoformat()}", flush=True)
        stores_frame = self.bucket.fetch_csv(STORES_SOURCE_FILE)
        print("Loaded stores.csv from S3", flush=True)
        sales_frame = self.bucket.fetch_csv(
            sales_key_for_month(sale_month),
            parse_dates=["date"],
        )
        print(f"Loaded sales file for {sale_month.isoformat()} from S3", flush=True)

        prepared_sales_frame = sales_frame.copy()
        prepared_sales_frame["date"] = pd.to_datetime(
            prepared_sales_frame["date"]
        ).dt.date

        monthly_sales_frame = build_monthly_sales_frame(
            sales_frame=prepared_sales_frame,
            stores_frame=stores_frame,
            sale_month=sale_month,
        )

        print("Replacing stores reference table", flush=True)
        self.warehouse.replace_table("stores", stores_frame)
        print("Reloading monthly sales data into Postgres", flush=True)
        self.warehouse.load_sales_month(
            sale_month=sale_month,
            sales_frame=prepared_sales_frame,
            monthly_sales_frame=monthly_sales_frame,
        )
        print("Finished loading monthly sales data", flush=True)


class FeatureStoreETL(BaseETL):
    """Build the feature store expected by the data science module."""

    def run(self) -> None:
        profiles_frame = self.warehouse.read_table("customer_profiles")
        activity_frame = self.warehouse.read_table("customer_activity")
        labels_frame = self.warehouse.read_table("labels")

        feature_store_frame = build_feature_store_frame(
            profiles_frame=profiles_frame,
            activity_frame=activity_frame,
            labels_frame=labels_frame,
        )
        self.warehouse.replace_table("feature_store", feature_store_frame)
