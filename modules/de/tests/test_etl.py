# Unit tests for DE ETL coordination logic.

import pandas as pd

from de_pipeline.etl import CustomerDataETL


class StubBucket:
    """Return predefined DataFrames for ETL tests."""

    def __init__(self, frames: dict[str, pd.DataFrame]) -> None:
        self.frames = frames

    def fetch_csv(self, key: str) -> pd.DataFrame:
        return self.frames[key]


class StubWarehouse:
    """Capture table writes made by ETL flows."""

    def __init__(self) -> None:
        self.writes: list[tuple[str, pd.DataFrame]] = []

    def replace_table(self, table_name: str, frame: pd.DataFrame) -> None:
        self.writes.append((table_name, frame.copy()))


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
