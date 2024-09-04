import pandas
from pandas import DataFrame
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError as SQLAlchemyProgrammingError

from dagster import (
    Any,
    ConfigurableIOManager,
    Field,
    StringSource,
    io_manager,
    get_dagster_logger,
)
import dagster._check as check

POSTGRES_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


class PostgresIOManager(ConfigurableIOManager):
    def __init__(
        self,
        username,
        password,
        hostname,
        port,
        dbname,
        **data: Any
    ):
        super().__init__(**data)
        self.logger = get_dagster_logger()

        self.username = username
        self.password = password
        self.hostname = hostname
        self.port = port
        self.dbname = dbname

        self.engine = create_engine(
            f"postgresql+psycopg2://"
            f"{self.username}:{self.password}@{self.hostname}:{self.port}/{self.dbname}"  # noqa: E501
        )
        session_class = sessionmaker(self.engine)
        self.session = session_class()

    def _get_path(self, context) -> str:
        if context.has_asset_key:
            path = context.get_asset_identifier()
            context.log.debug(f"Asset identifier: {path}")

            self.database_name = path[0].replace("-", "_")

            if len(path) == 4:
                table_prefix = path[1].replace("-", "_")
                table_name = path[2].replace("-", "_")

                if table_prefix in table_name:
                    self.schema_name = table_name
                elif "daily_ga" in table_name:
                    self.schema_name = table_name.replace("daily_", "")
                else:
                    self.schema_name = f"{table_prefix}__{table_name}"
            else:
                self.schema_name = path[-2].replace("daily_", "")

        else:
            path = context.get_identifier()
            context.log.debug(f"Identifier: {path}")
            self.database_name = path[0].replace("-", "_")
            self.schema_name = path[-2].replace("daily_", "").replace("-", "_")

        context.log.debug(
            f"Generated path: {self.database_name}.{self.schema_name}"
        )
        return f"{self.database_name}.{self.schema_name}"

    def has_output(self, context):
        key = self._get_path(context)
        self.logger.debug(f"has_output called for {key}")
        return True

    def _rm_object(self, key, obj):

        where_statement = self._get_where_statement(obj)

        sql_statement = f"DELETE FROM {self.schema_name} "
        sql_statement += where_statement
        self.logger.debug(f"Delete on {where_statement} for key {key}")
        self.session.execute(text(sql_statement))
        self.session.commit()

    def _has_object(self, key, obj):

        where_statement = self._get_where_statement(obj)

        sql_statement = f"SELECT * FROM {self.schema_name} "
        sql_statement += where_statement

        try:
            results = self.session.execute(text(sql_statement)).fetchall()
            found_object = bool(len(results))

        except SQLAlchemyProgrammingError as e:
            self.logger.warning(e)
            found_object = False

        return found_object

    def _get_where_statement(self, obj):
        where_statement = "WHERE "

        partition_expr_values = obj[self.partition_expr]
        partition_expr_values = partition_expr_values.drop_duplicates()

        _has_previous_condition = False
        for index, row in partition_expr_values.iterrows():
            if _has_previous_condition:
                where_statement += " OR "

            _has_previous_partition_expr = False

            where_statement += "("

            for expr in self.partition_expr:
                if _has_previous_partition_expr:
                    where_statement += " AND "
                where_statement += f"{expr} = '{row[expr]}'"
                _has_previous_partition_expr = True

            _has_previous_condition = True

            where_statement += ")"

        return where_statement

    def load_input(self, context) -> DataFrame:
        key = self._get_path(context)

        self.logger.debug(
            f"Checking data from {key} for partition {context.partition_key}"
        )

        sql_statement = f"SELECT * FROM {self.schema_name} "

        if context.partition_key:
            sql_statement += f"WHERE partition_key = '{context.partition_key}'"

        obj = pandas.read_sql(sql_statement, con=self.engine.connect())

        return obj

    def handle_output(self, context, obj):
        key = self._get_path(context)

        if isinstance(context.dagster_type.typing_type, type(None)):
            check.invariant(
                obj is None,
                "Output had Nothing type or 'None' annotation, "
                "but handle_output received value "
                f"that was not None and was of type {type(obj)}.",
            )
            return None

        context.log.debug(f"Writing DB object at: {key}")

        if obj is not None:
            if self._has_object(key, obj):
                context.log.warning(f"Removing existing DB entries from {key}.")
                self._rm_object(key, obj)
            obj.to_sql(
                self.schema_name,
                con=self.engine.connect(),
                index=False,
                if_exists="append",
            )
            context.add_output_metadata(
                {
                    "database_name": self.database_name,
                    "schema_name": self.schema_name,
                    "num_rows": len(obj.index),
                }
                | context.metadata
            )

        else:
            context.add_output_metadata(
                {
                    "database_name": self.database_name,
                    "schema_name": self.schema_name,
                    "num_rows": 0,
                }
            )


@io_manager(
    config_schema={
        "username": Field(
            StringSource,
        ),
        "password": Field(
            StringSource,
        ),
        "hostname": Field(
            StringSource,
        ),
        "port": Field(
            StringSource,
        ),
        "dbname": Field(
            StringSource,
        ),
    }
)
def postgres_io_manager(init_context):
    username = init_context.resource_config.get("username")
    password = init_context.resource_config.get("password")
    hostname = init_context.resource_config.get("hostname")
    port = init_context.resource_config.get("port")
    dbname = init_context.resource_config.get("dbname")

    _postgres_io_manager = PostgresIOManager(
        username,
        password,
        hostname,
        port,
        dbname,
    )

    return _postgres_io_manager
