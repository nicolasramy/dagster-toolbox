from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn


# fmt: off
EstablishmentsDataFrame = create_dagster_pandas_dataframe_type(
    name="EstablishmentsDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.integer_column(
            "section_number"
        ),
        PandasColumn.string_column("section_name"),
        PandasColumn.string_column("department_number"),
        PandasColumn.string_column("approval_number"),
        PandasColumn.string_column("local_number"),
        PandasColumn.string_column("company_name"),
        PandasColumn.string_column("address"),
        PandasColumn.string_column("postal_code"),
        PandasColumn.string_column("city"),
        PandasColumn.string_column("category"),
        PandasColumn.string_column("associated_activities"),
        PandasColumn.string_column("species"),
    ]
)
# fmt: on
