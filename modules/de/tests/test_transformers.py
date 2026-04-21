# Unit tests for the pure DE transformation helpers.

from datetime import datetime
import pandas as pd

from de_pipeline.transformers import (
    build_feature_store_frame,
    build_monthly_sales_frame,
    resolve_previous_month_start,
)


def test_resolve_previous_month_start_returns_first_day_of_previous_month():
    result = resolve_previous_month_start(datetime(2026, 4, 21, 9, 30))

    assert result.isoformat() == "2026-03-01"


def test_build_monthly_sales_frame_aggregates_one_month_per_store():
    sales_frame = pd.DataFrame(
        {
            "idx": [1, 2, 3],
            "value": [10.0, 5.5, 4.5],
            "date": ["2026-03-01", "2026-03-02", "2026-03-03"],
            "store_idx": [1, 1, 2],
        }
    )
    stores_frame = pd.DataFrame(
        {
            "idx": [1, 2],
            "location": ["Lisbon", "London"],
        }
    )

    result = build_monthly_sales_frame(
        sales_frame=sales_frame,
        stores_frame=stores_frame,
        sale_month=pd.Timestamp("2026-03-01").date(),
    )

    assert result.to_dict(orient="records") == [
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


def test_build_feature_store_frame_keeps_only_latest_activity_per_client():
    profiles_frame = pd.DataFrame(
        {
            "idx": [10, 11],
            "attr_a": [1, 2],
            "attr_b": ["a", "b"],
            "attr_c": ["yes", "no"],
        }
    )
    activity_frame = pd.DataFrame(
        {
            "idx": [10, 10, 11],
            "valid_from": ["2024-01-01", "2025-01-01", "2024-01-01"],
            "valid_to": ["2024-12-31", None, None],
            "scd_a": [0.1, 0.7, 0.3],
            "scd_b": [1, 5, 2],
        }
    )
    labels_frame = pd.DataFrame(
        {
            "idx": [10, 11],
            "label": [1, 0],
        }
    )

    result = build_feature_store_frame(
        profiles_frame=profiles_frame,
        activity_frame=activity_frame,
        labels_frame=labels_frame,
    )

    assert result.to_dict(orient="records") == [
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
