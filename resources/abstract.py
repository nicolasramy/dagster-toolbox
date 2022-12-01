from io import BytesIO
from os import environ

from minio import Minio
from minio.commonconfig import CopySource
from minio.error import S3Error

from dagster import get_dagster_logger


class ObjectStorage:
    client = None

    hostname = None
    access_key = None
    secret_key = None

    bucket = None

    def __init__(self):
        self.logger = get_dagster_logger()

        self.hostname = environ.get("MINIO_SERVER_URL")
        self.access_key = environ.get("MINIO_ROOT_USER")
        self.secret_key = environ.get("MINIO_ROOT_PASSWORD")

        # fmt: off
        if self.hostname:
            self.hostname = (
                self.hostname.replace("http://", "").replace("https://", "")
            )
        # fmt: on

        self.client = Minio(
            self.hostname,
            secure=False,
            access_key=self.access_key,
            secret_key=self.secret_key,
        )

    def read(self, object_name):
        try:
            response = self.client.get_object(
                bucket_name=self.bucket,
                object_name=object_name,
            )
            content = BytesIO(response.read())
            response.close()
            response.release_conn()

        except S3Error as e:
            self.logger.error(f"Caught {e} for {self.bucket}/{object_name}")
            raise e

        return content

    def write(self, object_name, data, content_type, metadata=None):
        data_buffer = BytesIO(data)

        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_name,
            data=data_buffer,
            length=len(data),
            content_type=content_type,
            metadata=metadata,
        )

    def stat(self, object_name):
        try:
            return self.client.stat_object(
                bucket_name=self.bucket,
                object_name=object_name,
            )

        except S3Error as e:
            self.logger.error(f"Caught {e} for {self.bucket}/{object_name}")
            return False

    def scan(self, prefix, recursive=True):
        return self.client.list_objects(
            bucket_name=self.bucket,
            prefix=prefix,
            recursive=recursive,
        )

    def copy(self, from_path, to_bucket, to_path):
        self.client.copy_object(
            to_bucket, to_path, CopySource(self.bucket, from_path)
        )
