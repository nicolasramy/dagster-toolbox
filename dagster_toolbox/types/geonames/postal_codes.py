from dagster_pandas import create_dagster_pandas_dataframe_type, PandasColumn

PostalCodeDataFrame = create_dagster_pandas_dataframe_type(
    name="PostalCodeDataFrame",
    columns=[
        PandasColumn.datetime_column(
            "partition_key",
            is_required=True,
        ),
        PandasColumn.string_column(
            "country_code",
            # iso country code, 2 characters
        ),
        PandasColumn.string_column(
            "postal_code",
            # Postal code
        ),
        PandasColumn.string_column(
            "name",
            # Place name
        ),
        PandasColumn.string_column(
            "admin_name_1",
            # 1. order subdivision (state) varchar(100)
        ),
        PandasColumn.string_column(
            "admin_code_1",
            # 1. order subdivision (state) varchar(20)
        ),
        PandasColumn.string_column(
            "admin_name_2",
            # 2. order subdivision (county/province) varchar(100)
        ),
        PandasColumn.string_column(
            "admin_code_2",
            # 2. order subdivision (county/province) varchar(20)
        ),
        PandasColumn.string_column(
            "admin_name_3",
            # 3. order subdivision (community) varchar(100)
        ),
        PandasColumn.string_column(
            "admin_code_3",
            # 3. order subdivision (community) varchar(20)
        ),
        PandasColumn.float_column(
            "latitude",
            # estimated latitude (wgs84)
        ),
        PandasColumn.float_column(
            "longitude",
            # estimated longitude (wgs84)
        ),
        PandasColumn.float_column(
            "accuracy",
            # accuracy of lat/lng from 1 = estimated, 4 = geonameid,
            # 6 = centroid of addresses or shape
        ),
    ],
)
