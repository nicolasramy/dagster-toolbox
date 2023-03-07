import pandera
from pandera.typing import Series, String, Int, Float, DateTime

from dagster_pandera import pandera_schema_to_dagster_type


# fmt: off
class GAEventsDataFrame(pandera.SchemaModel):
    event_category: Series[String] = pandera.Field(
        nullable=True,
        description="The event category.",
    )
    event_action: Series[String] = pandera.Field(
        nullable=True,
        description="Event action.",
    )
    event_label: Series[String] = pandera.Field(
        nullable=True,
        description="Event label.",
    )
    total_events: Series[Int] = pandera.Field(
        nullable=True,
        description="The total number of events for the profile, "
                    "across all categories.",
    )
    unique_events: Series[Int] = pandera.Field(
        nullable=True,
        description="The number of unique events. "
                    "Events in different sessions are counted "
                    "as separate events.",
    )
    event_value: Series[Int] = pandera.Field(
        nullable=True,
        description="Total value of events for the profile.",
    )
    customer_key: Series[String] = pandera.Field(
        nullable=True,
        description="Customer Identification key.",
    )
    customer_name: Series[String] = pandera.Field(
        nullable=True,
        description="Customer name.",
    )
    view_id: Series[Int] = pandera.Field(
        nullable=True,
        description="Google Analytics ViewID.",
    )
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )


class GASessionsDataFrame(pandera.SchemaModel):
    continent: Series[String] = pandera.Field(
        nullable=True,
        description="Users' continent, derived from users' IP "
                    "addresses or Geographical IDs.",
    )
    country: Series[String] = pandera.Field(
        nullable=True,
        description="Users' country, derived from their IP "
                    "addresses or Geographical IDs.",
    )
    country_iso_code: Series[String] = pandera.Field(
        nullable=True,
        description="Users' country's ISO code (in ISO-3166-1 alpha-2 format), "
                    "derived from their IP addresses or Geographical IDs. "
                    "For example, BR for Brazil, CA for Canada.",
    )
    region: Series[String] = pandera.Field(
        nullable=True,
        description="Users' region, derived from their IP "
                    "addresses or Geographical IDs. "
                    "In U.S., a region is a state, New York, for example.",
    )
    region_iso_code: Series[String] = pandera.Field(
        nullable=True,
        description="Users' region ISO code in ISO-3166-2 format, "
                    "derived from their IP addresses or Geographical IDs.",
    )
    city: Series[String] = pandera.Field(
        nullable=True,
        description="Users' city, derived from their IP "
                    "addresses or Geographical IDs.",
    )
    page_path: Series[String] = pandera.Field(
        nullable=True,
        description="A page on the website specified by path and/or "
                    "query parameters. Use this with hostname "
                    "to get the page's full URL.",
    )
    sessions: Series[Int] = pandera.Field(
        nullable=True,
        description="The total number of sessions.",
    )
    bounces: Series[Int] = pandera.Field(
        nullable=True,
        description="The total number of single page "
                    "(or single interaction hit) sessions for the property.",
    )
    sessions_per_user: Series[Float] = pandera.Field(
        nullable=True,
        description="The total number of sessions divided by "
                    "the total number of users.",
    )
    session_duration: Series[Float] = pandera.Field(
        nullable=True,
        description="Total duration (in seconds) of users' sessions.",
    )
    page_load_time: Series[Int] = pandera.Field(
        nullable=True,
        description="Total time (in milliseconds), from pageview initiation "
                    "(e.g., a click on a page link) to page load completion "
                    "in the browser, the pages in the sample set take to load.",
    )
    customer_key: Series[String] = pandera.Field(
        nullable=True,
        description="Customer Identification key.",
    )
    customer_name: Series[String] = pandera.Field(
        nullable=True,
        description="Customer name.",
    )
    view_id: Series[Int] = pandera.Field(
        nullable=True,
        description="Google Analytics ViewID.",
    )
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )


class GAUsersDataFrame(pandera.SchemaModel):
    continent: Series[String] = pandera.Field(
        nullable=True,
        description="Users' continent, derived from users' IP "
                    "addresses or Geographical IDs.",
    )
    country: Series[String] = pandera.Field(
        nullable=True,
        description="Users' country, derived from their IP "
                    "addresses or Geographical IDs.",
    )
    country_iso_code: Series[String] = pandera.Field(
        nullable=True,
        description="Users' country's ISO code (in ISO-3166-1 alpha-2 format), "
                    "derived from their IP addresses or Geographical IDs. "
                    "For example, BR for Brazil, CA for Canada.",
    )
    region: Series[String] = pandera.Field(
        nullable=True,
        description="Users' region, derived from their IP "
                    "addresses or Geographical IDs. "
                    "In U.S., a region is a state, New York, for example.",
    )
    region_iso_code: Series[String] = pandera.Field(
        nullable=True,
        description="Users' region ISO code in ISO-3166-2 format, "
                    "derived from their IP addresses or Geographical IDs.",
    )
    city: Series[String] = pandera.Field(
        nullable=True,
        description="Users' city, derived from their IP "
                    "addresses or Geographical IDs.",
    )
    page_path: Series[String] = pandera.Field(
        nullable=True,
        description="A page on the website specified by path and/or "
                    "query parameters. Use this with hostname "
                    "to get the page's full URL.",
    )
    users: Series[Int] = pandera.Field(
        nullable=True,
        description="The total number of users for the requested time period.",
    )
    new_users: Series[Int] = pandera.Field(
        nullable=True,
        description="The number of sessions marked as a user's first sessions.",
    )
    percent_new_sessions: Series[Float] = pandera.Field(
        nullable=True,
        description="The percentage of sessions by users who had never "
                    "visited the property before.",
    )
    sessions_per_user: Series[Float] = pandera.Field(
        nullable=True,
        description="The total number of sessions divided by "
                    "the total number of users.",
    )
    session_duration: Series[Float] = pandera.Field(
        nullable=True,
        description="Total duration (in seconds) of users' sessions.",
    )
    page_load_time: Series[Int] = pandera.Field(
        nullable=True,
        description="Total time (in milliseconds), from pageview initiation "
                    "(e.g., a click on a page link) to page load completion "
                    "in the browser, the pages in the sample set take to load.",
    )
    customer_key: Series[String] = pandera.Field(
        nullable=True,
        description="Customer Identification key.",
    )
    customer_name: Series[String] = pandera.Field(
        nullable=True,
        description="Customer name.",
    )
    view_id: Series[Int] = pandera.Field(
        nullable=True,
        description="Google Analytics ViewID.",
    )
    partition_key: Series[DateTime] = pandera.Field(
        nullable=True,
        description="Current partition.",
    )


GAEventsDataFrameType = pandera_schema_to_dagster_type(GAEventsDataFrame)
GASessionsDataFrameType = pandera_schema_to_dagster_type(GASessionsDataFrame)
GAUsersDataFrameType = pandera_schema_to_dagster_type(GAUsersDataFrame)
# fmt: on
