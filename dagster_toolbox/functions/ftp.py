import ftplib
from hashlib import sha512
from io import BytesIO

from slugify import slugify

from .partitions import get_current_partition


def prepare_object(file_resource):
    file_last_access = None
    file_last_modification = None
    file_size = len(file_resource)

    partition_key = get_current_partition()

    metadata = {
        "last_access": file_last_access,
        "last_modification": file_last_modification,
        "size": file_size,
        "partition": partition_key,
    }

    return partition_key, metadata


def is_file(ftp_client, filename):
    try:
        return ftp_client.size(filename) is not None

    except ftplib.error_perm:
        return False


# fmt: off
def ftp_get(
    context,
    ftp_client,
    path,
    destination,
    partitioned,
    files,
):
    context.log.debug(f"Open {path}")

    ftp_client.cwd(path)
    for filename in ftp_client.nlst():
        context.log.debug(filename)
        remote_path = f"/{path}/{filename}"

        if not is_file(ftp_client, remote_path):
            context.log.debug(f"{filename} skipped...")
            continue

        buffer = BytesIO()
        ftp_client.retrbinary(
            f"RETR {remote_path}",
            callback=buffer.write
        )

        slugify_filename = slugify(filename)

        if len(slugify_filename) <= 4:
            context.log.warning(
                f"Unable to parse filename {filename}"
            )
            continue

        if slugify_filename[-4] != "-":
            context.log.warning(
                f"Unable to parse extension for {filename}"
            )
            continue

        object_filename = ".".join(
            [slugify_filename[:-4], slugify_filename[-4:][1:]]
        )

        if partitioned:
            current_partition = get_current_partition()
            object_name = f"{destination}/{current_partition}/{path}/{object_filename}"  # noqa: E501

        else:
            object_name = f"{destination}/{path}/{object_filename}"

        object_name = object_name.replace("./", "").lower()

        raw_data = buffer.getvalue()
        file_hash = sha512(raw_data).hexdigest()

        partition_key, metadata = prepare_object(
            raw_data,
        )
        metadata["hash"] = file_hash

        file_to_append = {
            "name": object_name,
            "filename": filename,
            "hash": file_hash,
            "partition_key": partition_key,
            "is_new": False,
        }

        object_stat = context.resources.legacy_objects.stat(object_name)
        if object_stat:
            context.log.debug(f"{object_name} already exists")
            # Update object or create a new version

            if (
                metadata["hash"]
                == object_stat.metadata["x-amz-meta-hash"]
            ):
                context.log.debug(
                    f"{filename} and {object_name} seems to be the same"  # noqa: E501
                )
                files.append(file_to_append)
                continue

        context.log.info(
            f"Upload {filename} to s3 as {object_name}..."
        )

        context.resources.legacy_objects.write(
            object_name,
            raw_data,
            "text/csv",
            metadata,
        )
        file_to_append["is_new"] = True
        files.append(file_to_append)
# fmt: on
