from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

PostCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="PostCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column("name"),
        PandasColumn.string_column("slug"),
        PandasColumn.string_column("description"),
        PandasColumn.string_column("country_iso_code"),
        PandasColumn.string_column("region_iso_code"),
        PandasColumn.string_column("sub_region_code"),
        PandasColumn.string_column("code"),
    ],
)
