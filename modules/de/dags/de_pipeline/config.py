# Configuration objects for the DE pipelines.

from dataclasses import dataclass, field
from datetime import date
import os


CUSTOMER_SOURCE_FILES = (
    "customer_profiles.csv",
    "customer_activity.csv",
    "labels.csv",
)
STORES_SOURCE_FILE = "stores.csv"
PUBLIC_BUCKET_NAME = "daredata-technical-challenge-data"


def required_env(name: str) -> str:
    """Return a required environment variable or raise a clear error."""

    value = os.getenv(name)
    if value:
        return value
    raise RuntimeError(f"Environment variable {name} must be set")


@dataclass(frozen=True)
class DatabaseSettings:
    """Runtime settings used to connect to the operational database."""

    host: str = field(default_factory=lambda: os.getenv("ADMIN_DB_HOST", "operational-db"))
    port: int = field(default_factory=lambda: int(os.getenv("ADMIN_DB_PORT", "5432")))
    database: str = field(default_factory=lambda: os.getenv("ADMIN_DB_NAME", "companydata"))
    username: str = field(default_factory=lambda: required_env("ADMIN_DB_USER"))
    password: str = field(default_factory=lambda: required_env("ADMIN_DB_PASSWORD"))


@dataclass(frozen=True)
class StorageSettings:
    """Runtime settings for the source data bucket."""

    bucket_name: str = PUBLIC_BUCKET_NAME


def sales_key_for_month(sale_month: date) -> str:
    """Build the source object key for a monthly sales file."""

    return f"sales/{sale_month.isoformat()}/sales.csv"
