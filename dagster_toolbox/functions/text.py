import re

from slugify import slugify


CAMEL_CASE_TO_SNAKE_CASE = r"(?<!^)(?=[A-Z])"


def normalize_header(value):
    """
    columns = [text.normalize_header(column) for column in dataframe.columns]
    dataframe.columns = columns
    """
    value = re.sub(CAMEL_CASE_TO_SNAKE_CASE, "_", value).lower()
    value = slugify(value, separator="_")
    return value


def snakify(value):
    return slugify(value, separator="_").lower()


def remove_header_infixes(value, infexes):
    """
    infexes = ["ab:", "cd:", "ef:",]
    columns = [
        text.remove_header_infixes(column, infexes)
        for column in dataframe.columns
    ]
    dataframe.columns = columns
    """
    for infix in infexes:
        value = value.replace(infix, "")
