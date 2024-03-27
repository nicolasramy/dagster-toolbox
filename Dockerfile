FROM python:3.10-slim-bullseye


LABEL maintainer="nicolas.ramy@darkelda.com"

ENV PYTHONDONTWRITEBYTECODE 1

ENV DAGSTER_HOME /app

RUN mkdir /app


COPY . /app
WORKDIR /app


VOLUME ["/app"]
