from datetime import datetime
from hashlib import sha512
import stat

from slugify import slugify

from .partitions import get_current_partition


def prepare_object(file_resource, partitioned):
    file_stat = file_resource.stat()
    file_last_access = file_stat.st_atime
    file_last_modification = file_stat.st_mtime
    file_size = file_stat.st_size

    if partitioned:
        partition_key = get_current_partition()

    else:
        partition_key = datetime.fromtimestamp(file_last_modification).strftime(
            "%Y-%m-%d"
        )

    metadata = {
        "last_access": file_last_access,
        "last_modification": file_last_modification,
        "size": file_size,
        "partition": partition_key,
    }

    return partition_key, metadata


# fmt: off
def sftp_get_recursive(
    context,
    sftp_client,
    path,
    destination,
    partitioned,
    files,
):
    context.log.debug(f"Open {path}")
    for item in sftp_client.listdir_attr(path):
        remote_path = f"{path}/{item.filename}"
        mode = item.st_mode

        if stat.S_ISDIR(mode):
            sftp_get_recursive(
                context,
                sftp_client,
                remote_path,
                destination,
                partitioned,
                files,
            )

        elif stat.S_ISREG(mode):
            with sftp_client.file(remote_path, mode="r") as file_resource:
                slugify_filename = slugify(item.filename)

                if len(slugify_filename) <= 4:
                    context.log.warning(
                        f"Unable to parse filename {item.filename}"
                    )
                    continue

                if slugify_filename[-4] != "-":
                    context.log.warning(
                        f"Unable to parse extension for {item.filename}"
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

                raw_data = file_resource.read()
                file_hash = sha512(raw_data).hexdigest()

                partition_key, metadata = prepare_object(
                    file_resource,
                    partitioned,
                )
                metadata["hash"] = file_hash

                file_to_append = {
                    "name": object_name,
                    "filename": item.filename,
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
                            f"{item.filename} and {object_name} seems to be the same"  # noqa: E501
                        )
                        files.append(file_to_append)
                        continue

                context.log.info(
                    f"Upload {item.filename} to s3 as {object_name}..."
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
