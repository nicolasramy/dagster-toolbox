from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

CountryDataFrame = create_dagster_pandas_dataframe_type(
    name="CountryDataFrame",
    columns=[
        PandasColumn.integer_column("id"),
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.datetime_column(
            "activated",
            is_required=True,
        ),
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.datetime_column(
            "created",
            is_required=True,
        ),
        PandasColumn.datetime_column(
            "updated",
            is_required=False,
        ),
        PandasColumn.datetime_column(
            "activated",
            is_required=False,
        ),
        PandasColumn.string_column("name"),
        PandasColumn.string_column("slug"),
        PandasColumn.string_column("description"),
        PandasColumn.string_column("timezones"),
        PandasColumn.string_column("iso_code_2"),
        PandasColumn.string_column("iso_code_3"),
        PandasColumn.string_column("phone_prefix"),
        PandasColumn.string_column("continent"),
    ],
)
