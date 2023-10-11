from .abstract import ObjectStorage
from dagster import resource


class Analytics(ObjectStorage):
    bucket = "analytics"


@resource
def analytics_objects(init_context):
    return Analytics()


class Connecting(ObjectStorage):
    bucket = "connecting"


@resource
def connecting_objects(init_context):
    return Connecting()


class Customers(ObjectStorage):
    bucket = "customers"


@resource
def customers_objects(init_context):
    return Customers()


class Datalake(ObjectStorage):
    bucket = "datalake"


@resource
def datalake_objects(init_context):
    return Datalake()


class DataWarehouse(ObjectStorage):
    bucket = "datawarehouse"


@resource
def datawarehouse_objects(init_context):
    return DataWarehouse()


class Experiments(ObjectStorage):
    bucket = "experiments"


@resource
def experiments_objects(init_context):
    return Experiments()


class ExternalSources(ObjectStorage):
    bucket = "external-sources"


@resource
def external_sources_objects(init_context):
    return ExternalSources()


class Legacy(ObjectStorage):
    bucket = "legacy"


@resource
def legacy_objects(init_context):
    return Legacy()


class Logs(ObjectStorage):
    bucket = "logs"


@resource
def logs_objects(init_context):
    return Logs()


class Miscellaneous(ObjectStorage):
    bucket = "miscellaneous"


@resource
def miscellaneous_objects(init_context):
    return Miscellaneous()


class Test(ObjectStorage):
    bucket = "test"


@resource
def test_objects(init_context):
    return Test()
