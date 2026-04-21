#!/usr/bin/env bash
set -euo pipefail

# Initialize the Airflow metadata database the first time the container starts.
airflow db migrate

# Re-running the container should not fail if the admin user already exists.
airflow users create \
  --username airflow \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email airflow@example.com \
  --password airflow || true

# A single-container setup is enough for the challenge and keeps the local stack small.
airflow scheduler &
exec airflow webserver --port 8080
