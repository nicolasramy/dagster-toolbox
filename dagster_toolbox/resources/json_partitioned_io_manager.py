from io import BytesIO

import pandas

from dagster import (
    Any,
    ConfigurableIOManager,
    io_manager,
    MetadataValue,
    Field,
    StringSource,
    get_dagster_logger,
)

from dagster import check


class JsonPartitionedIOManager(ConfigurableIOManager):
    def __init__(self, s3_bucket, s3_session, s3_prefix=None, **data: Any):
        super().__init__(**data)
        self.logger = get_dagster_logger()

        self.bucket = check.str_param(s3_bucket, "s3_bucket")
        self.s3_prefix = check.opt_str_param(s3_prefix, "s3_prefix")
        self.s3 = s3_session
        self.s3.list_objects(Bucket=self.bucket, MaxKeys=1)

    def _get_path(self, context) -> str:
        if context.has_asset_key:
            path = context.get_asset_identifier()
            try:
                del path[path.index(self.bucket)]

            except ValueError:
                bucket_key = self.bucket.replace("-", "_")
                del path[path.index(bucket_key)]

        else:
            path = ["storage", *context.get_identifier()]

        return "/".join(path) + ".json"

    def has_output(self, context):
        key = self._get_path(context)
        return self._has_object(key)

    def _rm_object(self, key):
        check.str_param(key, "key")
        check.param_invariant(len(key) > 0, "key")

        # delete_object wont fail even if the item has been deleted.
        self.s3.delete_object(Bucket=self.bucket, Key=key)

    def _has_object(self, key):
        check.str_param(key, "key")
        check.param_invariant(len(key) > 0, "key")

        try:
            self.s3.get_object(Bucket=self.bucket, Key=key)
            found_object = True
        except self.s3.exceptions.NoSuchKey:
            found_object = False

        return found_object

    def _uri_for_key(self, key):
        check.str_param(key, "key")
        return "s3://" + self.bucket + "/" + "{key}".format(key=key)

    def load_input(self, context) -> pandas.DataFrame:
        if isinstance(context.dagster_type.typing_type, type(None)):
            return None

        key = self._get_path(context)
        if not self._has_object(key):
            context.log.warning(
                f"Object not found from {self._uri_for_key(key)}"
            )
            return None

        context.log.debug(f"Loading S3 object from: {self._uri_for_key(key)}")

        stream_bytes = BytesIO(
            self.s3.get_object(Bucket=self.bucket, Key=key)["Body"].read()
        )

        obj = pandas.read_json(
            stream_bytes,
            orient="records",
            encoding="utf-8",
        )

        return obj

    def handle_output(self, context, obj):
        if isinstance(context.dagster_type.typing_type, type(None)):
            check.invariant(
                obj is None,
                "Output had Nothing type or 'None' annotation, "
                "but handle_output received value "
                f"that was not None and was of type {type(obj)}.",
            )
            return None

        key = self._get_path(context)
        path = self._uri_for_key(key)
        context.log.debug(f"Writing S3 object at: {path}")

        if self._has_object(key):
            context.log.warning(f"Removing existing S3 key: {key}")
            self._rm_object(key)

        if obj is not None:
            pickled_obj = obj.to_json(
                orient="records",
                date_format="iso",
            )

            pickled_obj_bytes = BytesIO(bytes(pickled_obj, "utf-8"))
            self.s3.upload_fileobj(pickled_obj_bytes, self.bucket, key)
            context.add_output_metadata(
                {"uri": MetadataValue.path(path)} | context.metadata
            )

        else:
            context.add_output_metadata(
                {"uri": MetadataValue.path(path), "num_rows": 0}
            )


@io_manager(
    config_schema={
        "s3_bucket": Field(StringSource),
        "s3_prefix": Field(StringSource, is_required=False, default_value=""),
    },
    required_resource_keys={"s3"},
)
def json_partitioned_io_manager(init_context):
    s3_session = init_context.resources.s3
    s3_bucket = init_context.resource_config.get("s3_bucket")
    s3_prefix = init_context.resource_config.get("s3_prefix")

    _json_partitioned_io_manager = JsonPartitionedIOManager(
        s3_bucket, s3_session, s3_prefix=s3_prefix
    )
    return _json_partitioned_io_manager
