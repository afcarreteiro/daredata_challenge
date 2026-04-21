# Unit tests for DE ETL coordination logic.

from datetime import datetime

import pandas as pd

from de_pipeline.etl import CustomerDataETL, FeatureStoreETL, SalesDataETL


class StubBucket:
    """Return predefined DataFrames for ETL tests."""

    def __init__(self, frames: dict[str, pd.DataFrame]) -> None:
        self.frames = frames

    def fetch_csv(
        self,
        key: str,
        parse_dates: list[str] | None = None,
    ) -> pd.DataFrame:
        return self.frames[key]


class StubWarehouse:
    """Capture table writes made by ETL flows."""

    def __init__(self) -> None:
        self.writes: list[tuple[str, pd.DataFrame]] = []
        self.sales_loads: list[dict[str, object]] = []
        self.tables: dict[str, pd.DataFrame] = {}

    def replace_table(self, table_name: str, frame: pd.DataFrame) -> None:
        copied_frame = frame.copy()
        self.writes.append((table_name, copied_frame))
        self.tables[table_name] = copied_frame

    def load_sales_month(
        self,
        sale_month,
        sales_frame: pd.DataFrame,
        monthly_sales_frame: pd.DataFrame,
    ) -> None:
        self.sales_loads.append(
            {
                "sale_month": sale_month,
                "sales_frame": sales_frame.copy(),
                "monthly_sales_frame": monthly_sales_frame.copy(),
            }
        )

    def read_table(self, table_name: str) -> pd.DataFrame:
        return self.tables[table_name].copy()


def test_customer_data_etl_loads_source_into_same_name_table() -> None:
    frame = pd.DataFrame({"idx": [1], "label": [0]})
    warehouse = StubWarehouse()
    bucket = StubBucket({"labels.csv": frame})

    etl = CustomerDataETL(warehouse=warehouse, bucket=bucket)
    etl.load_source_file("labels.csv")

    assert len(warehouse.writes) == 1
    table_name, written_frame = warehouse.writes[0]
    assert table_name == "labels"
    assert written_frame.to_dict(orient="records") == [{"idx": 1, "label": 0}]


def test_sales_data_etl_reloads_previous_month_and_stores_reference_data() -> None:
    warehouse = StubWarehouse()
    bucket = StubBucket(
        {
            "stores.csv": pd.DataFrame(
                {
                    "idx": [1, 2],
                    "location": ["Lisbon", "London"],
                }
            ),
            "sales/2026-03-01/sales.csv": pd.DataFrame(
                {
                    "idx": [1, 2, 3],
                    "value": [10.0, 5.5, 4.5],
                    "date": ["2026-03-01", "2026-03-02", "2026-03-03"],
                    "store_idx": [1, 1, 2],
                }
            ),
        }
    )

    etl = SalesDataETL(warehouse=warehouse, bucket=bucket)
    etl.run(reference_datetime=datetime(2026, 4, 21, 9, 30))

    assert warehouse.writes[0][0] == "stores"
    assert len(warehouse.sales_loads) == 1

    sales_load = warehouse.sales_loads[0]
    assert sales_load["sale_month"].isoformat() == "2026-03-01"
    assert sales_load["sales_frame"].to_dict(orient="records") == [
        {
            "idx": 1,
            "value": 10.0,
            "date": pd.Timestamp("2026-03-01").date(),
            "store_idx": 1,
        },
        {
            "idx": 2,
            "value": 5.5,
            "date": pd.Timestamp("2026-03-02").date(),
            "store_idx": 1,
        },
        {
            "idx": 3,
            "value": 4.5,
            "date": pd.Timestamp("2026-03-03").date(),
            "store_idx": 2,
        },
    ]
    assert sales_load["monthly_sales_frame"].to_dict(orient="records") == [
        {
            "store_idx": 1,
            "location": "Lisbon",
            "sale_month": pd.Timestamp("2026-03-01").date(),
            "value": 15.5,
        },
        {
            "store_idx": 2,
            "location": "London",
            "sale_month": pd.Timestamp("2026-03-01").date(),
            "value": 4.5,
        },
    ]


def test_feature_store_etl_builds_and_replaces_feature_store_table() -> None:
    warehouse = StubWarehouse()
    warehouse.tables = {
        "customer_profiles": pd.DataFrame(
            {
                "idx": [10, 11],
                "attr_a": [1, 2],
                "attr_b": ["a", "b"],
            }
        ),
        "customer_activity": pd.DataFrame(
            {
                "idx": [10, 10, 11],
                "valid_from": ["2024-01-01", "2025-01-01", "2024-01-01"],
                "valid_to": ["2024-12-31", None, None],
                "scd_a": [0.1, 0.7, 0.3],
                "scd_b": [1, 5, 2],
            }
        ),
        "labels": pd.DataFrame(
            {
                "idx": [10, 11],
                "label": [1, 0],
            }
        ),
    }

    etl = FeatureStoreETL(warehouse=warehouse, bucket=StubBucket({}))
    etl.run()

    assert warehouse.writes[-1][0] == "feature_store"
    assert warehouse.writes[-1][1].to_dict(orient="records") == [
        {
            "idx": 10,
            "attr_a": 1,
            "attr_b": "a",
            "scd_a": 0.7,
            "scd_b": 5,
            "label": 1,
        },
        {
            "idx": 11,
            "attr_a": 2,
            "attr_b": "b",
            "scd_a": 0.3,
            "scd_b": 2,
            "label": 0,
        },
    ]
