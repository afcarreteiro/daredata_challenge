#!/usr/bin/env bash
set -euo pipefail

: "${AIRFLOW_ADMIN_USERNAME:?AIRFLOW_ADMIN_USERNAME must be set}"
: "${AIRFLOW_ADMIN_PASSWORD:?AIRFLOW_ADMIN_PASSWORD must be set}"

# Initialize the Airflow metadata database the first time the container starts.
airflow db migrate

# Re-running the container should not fail if the admin user already exists.
airflow users create \
  --username "${AIRFLOW_ADMIN_USERNAME}" \
  --firstname "${AIRFLOW_ADMIN_FIRSTNAME:-Air}" \
  --lastname "${AIRFLOW_ADMIN_LASTNAME:-Flow}" \
  --role Admin \
  --email "${AIRFLOW_ADMIN_EMAIL:-airflow@example.com}" \
  --password "${AIRFLOW_ADMIN_PASSWORD}" || true

# A single-container setup is enough for the challenge and keeps the local stack small.
airflow scheduler &
exec airflow webserver --port 8080
