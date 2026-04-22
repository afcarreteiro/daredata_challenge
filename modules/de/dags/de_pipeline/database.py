# Database access layer for the DE pipelines.

from datetime import date
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from de_pipeline.config import DatabaseSettings


class PostgresWarehouse:
    """Encapsulate all database reads, writes, and grants for the DE module."""

    def __init__(self, settings: DatabaseSettings | None = None) -> None:
        self.settings = settings or DatabaseSettings()
        self._engine: Engine | None = None

    @property
    def engine(self) -> Engine:
        """Create the SQLAlchemy engine lazily so Airflow imports stay lightweight."""

        if self._engine is None:
            connection_url = (
                "postgresql+psycopg2://"
                f"{self.settings.username}:{self.settings.password}"
                f"@{self.settings.host}:{self.settings.port}/{self.settings.database}"
            )
            self._engine = create_engine(connection_url)

        return self._engine

    def read_table(self, table_name: str) -> pd.DataFrame:
        """Load a full table into a DataFrame."""

        return pd.read_sql_table(table_name, con=self.engine, schema="public")

    def replace_table(self, table_name: str, frame: pd.DataFrame) -> None:
        """Replace a table atomically from a DataFrame and re-apply grants."""

        with self.engine.begin() as connection:
            frame.to_sql(table_name, con=connection, if_exists="replace", index=False)
        self.grant_table_access(table_name)

    def load_sales_month(
        self,
        sale_month: date,
        sales_frame: pd.DataFrame,
        monthly_sales_frame: pd.DataFrame,
    ) -> None:
        """Reload one month's sales data by deleting that month and inserting it again."""

        next_month = pd.Timestamp(sale_month) + pd.offsets.MonthBegin(1)

        with self.engine.begin() as connection:
            self.ensure_sales_tables(connection)
            print(f"Deleting raw sales rows for {sale_month.isoformat()}", flush=True)
            connection.execute(
                text(
                    """
                    DELETE FROM sales
                    WHERE date >= :sale_month
                      AND date < :next_month
                    """
                ),
                {
                    "sale_month": sale_month,
                    "next_month": next_month.date(),
                },
            )
            print("Inserting raw sales rows", flush=True)
            sales_frame.to_sql(
                "sales",
                con=connection,
                if_exists="append",
                index=False,
            )

            print(
                f"Deleting monthly aggregates for {sale_month.isoformat()}", flush=True
            )
            connection.execute(
                text("DELETE FROM monthly_sales WHERE sale_month = :sale_month"),
                {"sale_month": sale_month},
            )
            print("Inserting monthly sales aggregates", flush=True)
            monthly_sales_frame.to_sql(
                "monthly_sales",
                con=connection,
                if_exists="append",
                index=False,
            )

        self.grant_table_access("sales")
        self.grant_table_access("monthly_sales")

    def ensure_sales_tables(self, connection) -> None:
        """Create the sales tables if they do not already exist."""

        statements = (
            """
            CREATE TABLE IF NOT EXISTS sales (
                idx INTEGER NOT NULL,
                value DOUBLE PRECISION NOT NULL,
                date DATE NOT NULL,
                store_idx INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS monthly_sales (
                store_idx INTEGER NOT NULL,
                location TEXT NOT NULL,
                sale_month DATE NOT NULL,
                value DOUBLE PRECISION NOT NULL
            )
            """,
        )

        for statement in statements:
            connection.execute(text(statement))

    def grant_table_access(self, table_name: str) -> None:
        """Re-apply the expected DS and MLE grants after table creation/replacement."""

        grant_statements = (
            f"GRANT SELECT ON TABLE public.{table_name} TO ds_user_role",
            f"GRANT ALL PRIVILEGES ON TABLE public.{table_name} TO mle_user_role",
        )

        with self.engine.begin() as connection:
            for statement in grant_statements:
                connection.execute(text(statement))
