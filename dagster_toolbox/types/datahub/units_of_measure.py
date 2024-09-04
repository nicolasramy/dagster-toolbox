import pandera
from pandera.typing import Series, String, DateTime

from dagster_pandera import pandera_schema_to_dagster_type


# fmt: off
class UnitsOfMeasureDataFrame(pandera.DataFrameModel):
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )
    level_and_category: Series[String] = pandera.Field(
        nullable=True,
        description="See levels.csv.",
    )
    sector: Series[String] = pandera.Field(
        nullable=True,
        description="Only for Levels 1 and 2.",
    )
    common_code: Series[String] = pandera.Field(
        nullable=True,
        description="UNECE code for the unit of measure.",
    )
    name: Series[String] = pandera.Field(
        nullable=True,
    )
    quantity: Series[String] = pandera.Field(
        nullable=True,
        description="Measured quantity, only for Levels 1 and 2.",
    )
    description: Series[String] = pandera.Field(
        nullable=True,
    )


class UnitsOfMeasureLevelsDataFrame(pandera.DataFrameModel):
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )
    level_and_category: Series[String] = pandera.Field(
        nullable=True,
        description="See levels.csv.",
    )
    description: Series[String] = pandera.Field(
        nullable=True,
    )


UnitsOfMeasureDataFrameType = pandera_schema_to_dagster_type(
    UnitsOfMeasureDataFrame
)
UnitsOfMeasureLevelsDataFrameType = pandera_schema_to_dagster_type(
    UnitsOfMeasureLevelsDataFrame
)
# fmt: on
