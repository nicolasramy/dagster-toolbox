from datetime import datetime
import re

from apiclient.discovery import build
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame


CAMEL_CASE_TO_SNAKE_CASE = r"(?<!^)(?=[A-Z])"


def normalize_header(value):
    return re.sub(
        CAMEL_CASE_TO_SNAKE_CASE, "_", value.replace("ga:", "")
    ).lower()


def connect_to_google_analytics(sa_credentials):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        sa_credentials,
        ["https://www.googleapis.com/auth/analytics.readonly"],
    )

    # Create a service object
    http = credentials.refresh(httplib2.Http())
    discovery_url = "https://analyticsreporting.googleapis.com/$discovery/rest"

    service = build(
        "analytics",
        "v4",
        http=http,
        discoveryServiceUrl=discovery_url,
    )

    return service


def extract(response):
    reports = response["reports"][0]

    # fmt: off
    columns = [
        normalize_header(dimension)
        for dimension in reports["columnHeader"]["dimensions"]
    ] + [
        normalize_header(metric["name"])
        for metric
        in reports["columnHeader"]["metricHeader"]["metricHeaderEntries"]
    ]
    # fmt: on

    rows = []
    try:
        for row in reports["data"]["rows"]:
            metrics = [
                value for metric in row["metrics"] for value in metric["values"]
            ]
            rows.append(row["dimensions"] + metrics)

    except KeyError:
        rows = []

    dataframe = DataFrame(columns=columns, data=rows)
    return dataframe


def prepare_body(view_id, date, metrics, dimensions):
    return {
        "reportRequests": [
            {
                "viewId": view_id,
                "dateRanges": [
                    {
                        "startDate": date,
                        "endDate": date,
                    }
                ],
                "metrics": [
                    {"expression": "ga:{}".format(metric)} for metric in metrics
                ],
                "dimensions": [
                    {"name": "ga:{}".format(dimension)}
                    for dimension in dimensions
                ],
                "pageSize": 1000,
            }
        ]
    }


def ga_events(
    sa_credentials,
    customer_name,
    customer_key,
    view_id,
    partition_key,
):
    service = connect_to_google_analytics(sa_credentials)

    response = (
        service.reports()
        .batchGet(
            body=prepare_body(
                view_id,
                partition_key,
                ["totalEvents", "uniqueEvents", "eventValue"],
                ["eventCategory", "eventAction", "eventLabel"],
            )
        )
        .execute()
    )

    dataframe = extract(response)
    dataframe_length = len(dataframe.index)
    view_id = int(view_id)
    partition_key_datetime = datetime.strptime(partition_key, "%Y-%m-%d")

    # fmt: off
    dataframe["event_category"] = dataframe["event_category"].astype(str)
    dataframe["event_action"] = dataframe["event_action"].astype(str)
    dataframe["event_label"] = dataframe["event_label"].astype(str)
    dataframe["total_events"] = dataframe["total_events"].astype(int)
    dataframe["unique_events"] = dataframe["unique_events"].astype(int)
    dataframe["event_value"] = dataframe["event_value"].astype(int)

    dataframe["customer_key"] = [customer_key] * dataframe_length
    dataframe["customer_name"] = [customer_name] * dataframe_length
    dataframe["view_id"] = [view_id] * dataframe_length
    dataframe["partition_key"] = [partition_key_datetime] * dataframe_length
    # fmt: on
    return dataframe


def ga_sessions(
    sa_credentials,
    customer_name,
    customer_key,
    view_id,
    partition_key,
):
    service = connect_to_google_analytics(sa_credentials)

    response = (
        service.reports()
        .batchGet(
            body=prepare_body(
                view_id,
                partition_key,
                [
                    "sessions",
                    "bounces",
                    "sessionsPerUser",
                    "sessionDuration",
                    "pageLoadTime",
                ],
                [
                    "continent",
                    "country",
                    "countryIsoCode",
                    "region",
                    "regionIsoCode",
                    "city",
                    "pagePath",
                ],
            )
        )
        .execute()
    )

    dataframe = extract(response)
    dataframe_length = len(dataframe.index)
    view_id = int(view_id)
    partition_key_datetime = datetime.strptime(partition_key, "%Y-%m-%d")

    # fmt: off
    dataframe["continent"] = dataframe["continent"].astype(str)
    dataframe["country"] = dataframe["country"].astype(str)
    dataframe["country_iso_code"] = dataframe["country_iso_code"].astype(str)
    dataframe["region"] = dataframe["region"].astype(str)
    dataframe["region_iso_code"] = dataframe["region_iso_code"].astype(str)
    dataframe["city"] = dataframe["city"].astype(str)
    dataframe["page_path"] = dataframe["page_path"].astype(str)
    dataframe["sessions"] = dataframe["sessions"].astype(int)
    dataframe["bounces"] = dataframe["bounces"].astype(int)
    dataframe["sessions_per_user"] = (
        dataframe["sessions_per_user"].astype(float)
    )
    dataframe["session_duration"] = (
        dataframe["session_duration"].astype(float)
    )
    dataframe["page_load_time"] = dataframe["page_load_time"].astype(int)

    dataframe["customer_key"] = [customer_key] * dataframe_length
    dataframe["customer_name"] = [customer_name] * dataframe_length
    dataframe["view_id"] = [view_id] * dataframe_length
    dataframe["partition_key"] = [partition_key_datetime] * dataframe_length
    # fmt: on
    return dataframe


def ga_users(
    sa_credentials,
    customer_name,
    customer_key,
    view_id,
    partition_key,
):
    service = connect_to_google_analytics(sa_credentials)

    response = (
        service.reports()
        .batchGet(
            body=prepare_body(
                view_id,
                partition_key,
                [
                    "users",
                    "newUsers",
                    "percentNewSessions",
                    "sessionsPerUser",
                    "sessionDuration",
                    "pageLoadTime",
                ],
                [
                    "continent",
                    "country",
                    "countryIsoCode",
                    "region",
                    "regionIsoCode",
                    "city",
                    "pagePath",
                ],
            )
        )
        .execute()
    )

    dataframe = extract(response)
    dataframe_length = len(dataframe.index)
    view_id = int(view_id)
    partition_key_datetime = datetime.strptime(partition_key, "%Y-%m-%d")

    # fmt: off
    dataframe["continent"] = dataframe["continent"].astype(str)
    dataframe["country"] = dataframe["country"].astype(str)
    dataframe["country_iso_code"] = dataframe["country_iso_code"].astype(str)
    dataframe["region"] = dataframe["region"].astype(str)
    dataframe["region_iso_code"] = dataframe["region_iso_code"].astype(str)
    dataframe["city"] = dataframe["city"].astype(str)
    dataframe["page_path"] = dataframe["page_path"].astype(str)
    dataframe["users"] = dataframe["users"].astype(int)
    dataframe["new_users"] = dataframe["new_users"].astype(int)
    dataframe["percent_new_sessions"] = (
        dataframe["percent_new_sessions"].astype(float)
    )
    dataframe["sessions_per_user"] = (
        dataframe["sessions_per_user"].astype(float)
    )
    dataframe["session_duration"] = dataframe["session_duration"].astype(float)
    dataframe["page_load_time"] = dataframe["page_load_time"].astype(int)

    dataframe["customer_key"] = [customer_key] * dataframe_length
    dataframe["customer_name"] = [customer_name] * dataframe_length
    dataframe["view_id"] = [view_id] * dataframe_length
    dataframe["partition_key"] = [partition_key_datetime] * dataframe_length
    # fmt: on
    return dataframe


def ga_events_dataframe(context, secret_path):
    secrets = context.resources.vault.get_data(secret_path)

    view_id = secrets["view_id"]
    sa_credentials = secrets["sa_credentials"]
    customer_name = secrets["customer_name"]
    partition_key = context.asset_partition_key_for_output()
    customer_key = secret_path.replace("analytics/google-analytics/", "")

    dataframe = ga_events(
        sa_credentials, customer_name, customer_key, view_id, partition_key
    )

    metadata = {
        "table": "ga_events",
        "partition_expr": "partition_key,customer_key",
        "partition_key": partition_key,
        "customer_key": customer_key,
        "view_id": view_id,
        "customer_name": customer_name,
    }

    if isinstance(dataframe, DataFrame):
        metadata["num_rows"] = len(dataframe.index)

    return dataframe, metadata


def ga_sessions_dataframe(context, secret_path):
    secrets = context.resources.vault.get_data(secret_path)

    view_id = secrets["view_id"]
    sa_credentials = secrets["sa_credentials"]
    customer_name = secrets["customer_name"]
    partition_key = context.asset_partition_key_for_output()
    customer_key = secret_path.replace("analytics/google-analytics/", "")

    dataframe = ga_sessions(
        sa_credentials, customer_name, customer_key, view_id, partition_key
    )

    metadata = {
        "table": "ga_sessions",
        "partition_expr": "partition_key,customer_key",
        "partition_key": partition_key,
        "customer_key": customer_key,
        "view_id": view_id,
        "customer_name": customer_name,
    }

    if isinstance(dataframe, DataFrame):
        metadata["num_rows"] = len(dataframe.index)

    return dataframe, metadata


def ga_users_dataframe(context, secret_path):
    secrets = context.resources.vault.get_data(secret_path)

    view_id = secrets["view_id"]
    sa_credentials = secrets["sa_credentials"]
    customer_name = secrets["customer_name"]
    partition_key = context.asset_partition_key_for_output()
    customer_key = secret_path.replace("analytics/google-analytics/", "")

    dataframe = ga_users(
        sa_credentials, customer_name, customer_key, view_id, partition_key
    )

    metadata = {
        "table": "ga_users",
        "partition_expr": "partition_key,customer_key",
        "partition_key": partition_key,
        "customer_key": customer_key,
        "view_id": view_id,
        "customer_name": customer_name,
    }

    if isinstance(dataframe, DataFrame):
        metadata["num_rows"] = len(dataframe.index)

    return dataframe, metadata
