from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

CountryDataFrame = create_dagster_pandas_dataframe_type(
    name="CountryDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column("name"),
        PandasColumn.string_column("slug"),
        PandasColumn.string_column("description"),
        PandasColumn.string_column("iso_code_2"),
        PandasColumn.string_column("iso_code_3"),
        PandasColumn.string_column("phone_prefix"),
        PandasColumn.string_column("continent_iso_code"),
        PandasColumn.integer_column("geoname_id"),
    ],
)
