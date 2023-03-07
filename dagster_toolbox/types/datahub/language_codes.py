from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

LanguageCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="LanguageCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "alpha3_b",
        ),
        PandasColumn.string_column(
            "alpha3_t",
        ),
        PandasColumn.string_column(
            "alpha2",
        ),
        PandasColumn.string_column(
            "english",
        ),
        PandasColumn.string_column(
            "french",
        ),
    ],
)
