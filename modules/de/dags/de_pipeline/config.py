# Configuration objects for the DE pipelines.

from dataclasses import dataclass
from datetime import date
import os


CUSTOMER_SOURCE_FILES = (
    "customer_profiles.csv",
    "customer_activity.csv",
    "labels.csv",
)
STORES_SOURCE_FILE = "stores.csv"
PUBLIC_BUCKET_NAME = "daredata-technical-challenge-data"


@dataclass(frozen=True)
class DatabaseSettings:
    """Runtime settings used to connect to the operational database."""

    host: str = os.getenv("ADMIN_DB_HOST", "operational-db")
    port: int = int(os.getenv("ADMIN_DB_PORT", "5432"))
    database: str = os.getenv("ADMIN_DB_NAME", "companydata")
    username: str = os.getenv("ADMIN_DB_USER", "admin")
    password: str = os.getenv("ADMIN_DB_PASSWORD", "admin")


@dataclass(frozen=True)
class StorageSettings:
    """Runtime settings for the source data bucket."""

    bucket_name: str = PUBLIC_BUCKET_NAME


def sales_key_for_month(sale_month: date) -> str:
    """Build the source object key for a monthly sales file."""

    return f"sales/{sale_month.isoformat()}/sales.csv"
