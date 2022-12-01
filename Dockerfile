FROM python:3.10-slim

LABEL maintainer="nicolas.ramy@connecting-food.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV DAGSTER_HOME /app
ENV GOOGLE_APPLICATION_CREDENTIALS /app/config/ga-credentials.json

ENV CELERY_VERSION 5.2.7
ENV DAGSTER_VERSION 1.0.17
ENV DAGSTER_LIBRAIRIES_VERSION 0.16.17
ENV DBT_POSTGRES_VERSION 1.3.1
ENV GOOGLE_API_PYTHON_CLIENT_VERSION 2.65.0
ENV HVAC_VERSION 1.0.2
ENV MINIO_VERSION 7.1.12
ENV NETWORKX_VERSION 2.8.8
ENV OAUTH2CLIENT_VERSION 4.1.3
ENV OPENPYXL_VERSION 3.0.10
ENV PANDAS_VERSION 1.5.1
ENV PEEWEE_VERSION 3.15.3
ENV PYTEST_VERSION 7.2.0
ENV PYTHON_SLUGIFY_VERSION 6.1.2
ENV REQUESTS_VERSION 2.28.1

# system update
RUN update-ca-certificates
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cron \
        gcc \
        git \
        libpq-dev \
        postgresql-client \
        postgresql-client-common \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install Celery==${CELERY_VERSION} \
        celery[gevent,librabbitmq]==${CELERY_VERSION} \
        dagit==${DAGSTER_VERSION} \
        dagster==${DAGSTER_VERSION} \
        dagster-aws==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-celery==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-dbt==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-ge==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-pandas==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-pandera==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-postgres==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-slack==${DAGSTER_LIBRAIRIES_VERSION} \
        dagster-ssh==${DAGSTER_LIBRAIRIES_VERSION} \
        dbt-postgres==${DBT_POSTGRES_VERSION} \
        google-api-python-client==${GOOGLE_API_PYTHON_CLIENT_VERSION} \
        hvac==${HVAC_VERSION} \
        minio==${MINIO_VERSION} \
        networkx==${NETWORKX_VERSION} \
        oauth2client==${OAUTH2CLIENT_VERSION} \
        openpyxl==${OPENPYXL_VERSION} \
        pandas==${PANDAS_VERSION} \
        pytest==${PYTEST_VERSION} \
        python-slugify==${PYTHON_SLUGIFY_VERSION} \
        peewee==${PEEWEE_VERSION} \
        pytest==${PYTEST_VERSION} \
        requests==${REQUESTS_VERSION}

RUN useradd -ms /bin/bash dagster

USER dagster

CMD ["bash"]
