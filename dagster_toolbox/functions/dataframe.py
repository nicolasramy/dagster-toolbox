from datetime import datetime


def cast_dataframe(dataframe, columns):
    for column_name, column_type in columns:
        if column_type == "string":
            dataframe[column_name] = dataframe[column_name].astype(
                "str", errors="ignore"
            )
        elif column_type == "int":
            dataframe[column_name] = dataframe[column_name].astype(
                "int", errors="ignore"
            )
        elif column_type == "float":
            dataframe[column_name] = dataframe[column_name].astype(
                "float", errors="ignore"
            )
        elif column_type == "bool":
            dataframe[column_name] = dataframe[column_name].astype(
                "bool", errors="ignore"
            )
        elif column_type == "datetime":
            dataframe[column_name] = dataframe[column_name].astype(
                "datetime", errors="ignore"
            )
        elif column_type == "timedelta":
            dataframe[column_name] = dataframe[column_name].astype(
                "timedelta", errors="ignore"
            )
        elif column_type == "category":
            dataframe[column_name] = dataframe[column_name].astype(
                "category", errors="ignore"
            )
        else:
            dataframe[column_name] = dataframe[column_name].astype(
                "str", errors="ignore"
            )

    return dataframe


def get_date(value):
    try:
        return datetime.strptime(value, "%d/%m/%Y")
    except ValueError:
        return value


def get_float_to_string(value):
    try:
        return str(int(float(value)))
    except ValueError:
        return value


def get_float_from_string(value):
    try:
        return float(value)
    except ValueError:
        return value


def get_int_from_string(value):
    try:
        return int(value)
    except ValueError:
        return value


def get_string_from_float(value):
    try:
        return str(int(float(value)))
    except ValueError:
        return value


def get_human_input_removed(value):
    if value == "...":
        return ""
    return value
