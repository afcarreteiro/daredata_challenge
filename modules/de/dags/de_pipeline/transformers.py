# Pure transformation helpers used by the DE ETLs.

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def resolve_previous_month_start(reference_datetime: datetime | None = None) -> date:
    """Return the first day of the month immediately before the reference date."""

    reference = reference_datetime or datetime.now()
    current_month_start = date(reference.year, reference.month, 1)

    return current_month_start - relativedelta(months=1)


def build_monthly_sales_frame(
    sales_frame: pd.DataFrame,
    stores_frame: pd.DataFrame,
    sale_month: date,
) -> pd.DataFrame:
    """Aggregate a month's sales by store and location."""

    sales_with_locations = sales_frame.merge(
        stores_frame.rename(columns={"idx": "store_idx"}),
        on="store_idx",
        how="left",
        validate="many_to_one",
    )
    sales_with_locations["sale_month"] = pd.Timestamp(sale_month).date()

    monthly_sales = (
        sales_with_locations.groupby(
            ["store_idx", "location", "sale_month"],
            as_index=False,
        )["value"]
        .sum()
        .sort_values(["store_idx", "location"])
        .reset_index(drop=True)
    )

    return monthly_sales


def build_feature_store_frame(
    profiles_frame: pd.DataFrame,
    activity_frame: pd.DataFrame,
    labels_frame: pd.DataFrame,
) -> pd.DataFrame:
    """Join customer data into the single-row-per-client feature store contract."""

    activity = activity_frame.copy()
    activity["valid_from"] = pd.to_datetime(activity["valid_from"])
    activity["valid_to"] = pd.to_datetime(activity["valid_to"])

    # A missing valid_to value represents the latest activity snapshot.
    activity["valid_to_sort"] = activity["valid_to"].fillna(
        pd.Timestamp.max.normalize()
    )

    latest_activity = activity.sort_values(
        ["idx", "valid_to_sort", "valid_from"],
        ascending=[True, False, False],
    ).drop_duplicates(subset=["idx"], keep="first")[["idx", "scd_a", "scd_b"]]

    feature_store = (
        profiles_frame[["idx", "attr_a", "attr_b"]]
        .merge(latest_activity, on="idx", how="inner", validate="one_to_one")
        .merge(
            labels_frame[["idx", "label"]], on="idx", how="inner", validate="one_to_one"
        )
        .sort_values("idx")
        .reset_index(drop=True)
    )

    return feature_store[["idx", "attr_a", "attr_b", "scd_a", "scd_b", "label"]]
