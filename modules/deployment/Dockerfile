FROM python:3.9

WORKDIR /app

ENV HOME=/app/runtime
ENV MODEL_DIR=/app/models
ENV PORT=5000

COPY modules/mle/mle_package /app/modules/mle/mle_package
RUN pip install /app/modules/mle/mle_package

COPY modules/ds/ds_package /app/modules/ds/ds_package
RUN pip install /app/modules/ds/ds_package

RUN pip install flask==3.0.3 gunicorn==22.0.0

COPY modules/deployment/api /app/api
COPY modules/ds/models /app/models

RUN mkdir -p /app/runtime/mle_storage

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api.app:app"]
