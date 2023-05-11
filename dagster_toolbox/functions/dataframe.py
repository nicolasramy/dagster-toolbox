def cast_dataframe(dataframe, columns):
    for column_name, column_type in columns:
        if column_type == "string":
            dataframe[column_name] = dataframe[column_name].astype(str)
        elif column_type == "float":
            dataframe[column_name] = dataframe[column_name].astype(float)
        else:
            dataframe[column_name] = dataframe[column_name].astype(str)

    return dataframe
