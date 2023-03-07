from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

ContainerCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="ContainerCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "code",
        ),
        PandasColumn.string_column(
            "description",
        ),
        PandasColumn.integer_column(
            "length",
        ),
        PandasColumn.integer_column(
            "height",
        ),
        PandasColumn.string_column(
            "group",
        ),
    ],
)

ContainerGroupDataFrame = create_dagster_pandas_dataframe_type(
    name="ContainerGroupDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "code",
        ),
        PandasColumn.string_column(
            "description",
        ),
    ],
)
