from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

ContinentCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="ContinentCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "code",
        ),
        PandasColumn.string_column(
            "name",
        ),
    ],
)
