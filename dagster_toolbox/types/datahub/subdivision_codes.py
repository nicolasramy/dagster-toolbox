import pandera
from pandera.typing import Series, String, DateTime

from dagster_pandera import pandera_schema_to_dagster_type


# fmt: off
class SubDivisionCodesDataFrame(pandera.DataFrameModel):
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )
    country: Series[String] = pandera.Field(
        nullable=True,
        description="Country ISO / Identification Code.",
    )
    code: Series[String] = pandera.Field(
        nullable=True,
        description="Sub Division UN Identification Code.",
    )
    name: Series[String] = pandera.Field(
        nullable=True,
        description="Sub Division name.",
    )


SubDivisionCodesDataFrameType = pandera_schema_to_dagster_type(
    SubDivisionCodesDataFrame
)
# fmt: on
