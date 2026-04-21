# Small wrapper around the public S3 bucket used by the challenge.

from io import BytesIO
from typing import Iterable
import boto3
from botocore import UNSIGNED
from botocore.client import Config
import pandas as pd

from de_pipeline.config import StorageSettings


class PublicS3Bucket:
    """Fetch CSV files from the public challenge bucket without AWS credentials."""

    def __init__(self, settings: StorageSettings | None = None) -> None:
        self.settings = settings or StorageSettings()
        self._client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

    def fetch_csv(
        self,
        key: str,
        parse_dates: Iterable[str] | None = None,
    ) -> pd.DataFrame:
        """Return the object contents as a pandas DataFrame."""

        response = self._client.get_object(
            Bucket=self.settings.bucket_name,
            Key=key,
        )

        status_code = response["ResponseMetadata"]["HTTPStatusCode"]

        if status_code != 200:
            raise Exception(f"Failed to fetch CSV from S3: {status_code}")

        print(f"Successful S3 get_object response. Status - {status_code}")
        body = response["Body"].read()
        return pd.read_csv(BytesIO(body), parse_dates=list(parse_dates or []))
