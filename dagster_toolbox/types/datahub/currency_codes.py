from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

CurrencyCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="CurrencyCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "entity",
        ),
        PandasColumn.string_column(
            "currency",
        ),
        PandasColumn.string_column(
            "alphabetic_code",
        ),
        PandasColumn.integer_column(
            "numeric_code",
        ),
        PandasColumn.integer_column(
            "minor_unit",
        ),
        PandasColumn.string_column(
            "withdrawal_date",
        ),
    ],
)
