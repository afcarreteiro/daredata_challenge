FROM apache/airflow:2.9.3-python3.11

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

USER root

COPY scripts/start-airflow.sh /opt/airflow/scripts/start-airflow.sh
RUN mkdir -p /opt/airflow/scripts \
    && sed -i 's/\r$//' /opt/airflow/scripts/start-airflow.sh \
    && chmod +x /opt/airflow/scripts/start-airflow.sh

USER airflow

ENV PYTHONPATH="/opt/airflow/dags:${PYTHONPATH}"

ENTRYPOINT ["/bin/bash", "/opt/airflow/scripts/start-airflow.sh"]
