---
title: Resources
author: Nicolas Ramy
date: 2023-03-07
layout: post
---



ObjectStorage
-------------

Declaration

```python
from dagster_toolbox.resources import ObjectStorage


class Analytics(ObjectStorage):
    bucket = "analytics"
    

@resource
def analytics_objects(init_context):
    return Analytics()


RESOURCE_DEFS = {
    "analytics_objects": analytics_objects,
}
```

Usage

```python
from dagster import asset


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    partition_key = context.asset_partition_key_for_output()
    file_path = f"analytics/data/{partition_key}"
    
    file_resource = context.resource.analytics_objects.read(file_path)
    ...
```

csv_partitioned_io_manager
-------------

Declaration

```python
from dagster_toolbox.resources import csv_partitioned_io_manager


RESOURCE_DEFS = {
    "csv_partitioned_io_manager": csv_partitioned_io_manager.configured(
        {
            "s3_bucket": "analytics",
        }
    ),
}
```

Usage

```python
from dagster import asset

from analytics.resource_defs import RESOURCE_DEFS


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    ...

```

json_partitioned_io_manager
-------------

Declaration

```python
from dagster_toolbox.resources import json_partitioned_io_manager


RESOURCE_DEFS = {
    "json_partitioned_io_manager": json_partitioned_io_manager.configured(
        {
            "s3_bucket": "analytics",
        }
    ),
}
```

Usage

```python
from dagster import asset

from analytics.resource_defs import RESOURCE_DEFS


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    ...

```

postgres_partitioned_io_manager
-------------

Declaration

```python
from dagster_toolbox.resources import postgres_partitioned_io_manager


RESOURCE_DEFS = {
    "postgres_partitioned_io_manager": postgres_partitioned_io_manager.configured(
        {
            "partition_expr": "customer_key,partition_key",
            "hostname": {
                "env": "POSTGRES_HOSTNAME",
            },
            "username": {
                "env": "POSTGRES_USER",
            },
            "password": {
                "env": "POSTGRES_PASSWORD",
            },
            "port": {
                "env": "POSTGRES_PORT",
            },
            "dbname": "analytics",
        }
    ),
}
```

Usage

```python
from dagster import asset

from analytics.resource_defs import RESOURCE_DEFS


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    ...

```

postgres_io_manager
-------------

Declaration

```python
from dagster_toolbox.resources import postgres_io_manager


RESOURCE_DEFS = {
    "postgres_io_manager": postgres_io_manager.configured(
        {
            "hostname": {
                "env": "POSTGRES_HOSTNAME",
            },
            "username": {
                "env": "POSTGRES_USER",
            },
            "password": {
                "env": "POSTGRES_PASSWORD",
            },
            "port": {
                "env": "POSTGRES_PORT",
            },
            "dbname": "analytics",
        }
    ),
}
```

Usage

```python
from dagster import asset

from analytics.resource_defs import RESOURCE_DEFS


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    ...

```

vault
-------------

Declaration

```python
from dagster_toolbox.resources import vault


RESOURCE_DEFS = {
    "vault": vault
}
```

Usage

```python
from dagster import asset

from analytics.resource_defs import RESOURCE_DEFS


@asset(resource_defs=RESOURCE_DEFS,)
def export_files(context):
    secrets = context.resources.vault.get_data(SECRET_PATH)
    ...

```
