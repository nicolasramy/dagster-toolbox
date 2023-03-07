import csv
from datetime import datetime
import fnmatch

import pandas

from .text import normalize_header


def datasource_dataframe(context, key, mapping):
    partition_key = context.asset_partition_key_for_output()
    prefix = mapping["prefix"]
    file_pattern = mapping["file_pattern"]

    partition_key_datetime = datetime.strptime(partition_key, "%Y-%m-%d")
    file_name = partition_key_datetime.strftime(file_pattern)

    object_name = f"{prefix}/{file_name}"

    encoding = mapping["encoding"]
    delimiter = mapping["delimiter"]
    skiprows = mapping["skiprows"]

    sftp_files_found = []
    dataframe = pandas.DataFrame()

    for row in context.resources.legacy_objects.scan(prefix):
        if fnmatch.fnmatch(row.object_name, object_name):
            sftp_files_found.append(row.object_name)
            context.log.debug(f"{row.object_name} found")

            file_resource = context.resources.legacy_objects.read(
                row.object_name
            )
            file_header = file_resource.read(2048).decode(encoding)
            context.log.debug(f"header of {row.object_name}:\n{file_header}")

            try:
                if csv.Sniffer().has_header(file_header):
                    additional_dataframe = pandas.read_csv(
                        context.resources.legacy_objects.read(row.object_name),
                        encoding=encoding,
                        delimiter=delimiter,
                        skiprows=skiprows,
                    )

                else:
                    context.log.warning(
                        f"No headers found in file {row.object_name}"
                    )
                    additional_dataframe = pandas.read_csv(
                        context.resources.legacy_objects.read(row.object_name),
                        encoding=encoding,
                        delimiter=delimiter,
                        skiprows=skiprows,
                        header=None,
                        names=mapping["columns"],
                    )
            except csv.Error:
                context.log.warning(f"Force header for file {row.object_name}")
                additional_dataframe = pandas.read_csv(
                    context.resources.legacy_objects.read(row.object_name),
                    encoding=encoding,
                    delimiter=delimiter,
                    skiprows=skiprows + 1,
                    header=None,
                    names=mapping["columns"],
                )

            dataframe = pandas.concat(
                [
                    dataframe,
                    additional_dataframe,
                ]
            )

    if not len(sftp_files_found):
        context.log.warning(f"{object_name} not found in SFTP files")
        return pandas.DataFrame(), {}

    dataframe.dropna(how="all", inplace=True)

    if dataframe.empty:
        context.log.warning("output dataframe is empty")
        return dataframe, {}

    columns = [normalize_header(column.lower()) for column in dataframe.columns]
    dataframe.columns = columns

    metadata = {
        "table": key,
        "partition_expr": "partition_key",
        "partition_key": partition_key,
        "sources": ", ".join(sftp_files_found),
    }

    dataframe_length = len(dataframe.index)
    partition_key_datetime = datetime.strptime(
        partition_key,
        "%Y-%m-%d",
    )

    # fmt: off
    dataframe["partition_key"] = [partition_key_datetime] * dataframe_length
    # fmt: on

    metadata["num_rows"] = dataframe_length

    return dataframe, metadata
