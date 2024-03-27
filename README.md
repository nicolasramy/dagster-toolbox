# Dagster Toolbox
A set of tools to ease Dagster usage

## Requirements

- Python 3.10+
- Dagster 1.6.13 / 0.22.13

## Installation

```shell
pip install dagster-toolbox
```

## Usage

#### New object storage resource

Declare resource

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

Use resource

```python
@asset
def export_files(context):
    partition_key = context.asset_partition_key_for_output()
    file_path = f"analytics/data/{partition_key}"
    
    file_resource = context.resource.analytics_objects.read(file_path)    
    ...

```
