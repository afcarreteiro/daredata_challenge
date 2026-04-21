"""
Functions to fetch the data from the DB.
"""

import os
import pandas as pd


def get_conn_string():
    """Gets a connection string to the database.
    """
    conn_string = f"postgresql+psycopg2://{os.environ['DS_DB_USER']}:{os.environ['DS_DB_PASSWORD']}@{os.environ['DB_HOSTNAME']}/companydata"
    return conn_string

def get_dataset():
    """Fetches the feature store from the database.
    """
    dataset = pd.read_sql(
        "select * from feature_store",
        get_conn_string()
    )

    return dataset