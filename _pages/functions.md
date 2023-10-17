---
title: Functions
author: Nicolas Ramy
date: 2022-12-01
layout: post
---


dataframe
-------------

### cast_dataframe

```python
def cast_dataframe(dataframe, columns):
    """
    columns = (
        ("column_a", "string",),
        ("column_b", "int",),
        ("column_c", "float",),
        ("column_d", "bool",),
        ("column_e", "datetime",),
        ("column_f", "timedelta",),
        ("column_g", "category",),
    )
    """
```

### get_date

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_date)
```

### get_float_to_string (deprecated)

Parse float transform to int and cast to string

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_float_to_string)
```

### get_float_from_string

Parse as float

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_float_from_string)
```

### get_int_from_string

Parse as int

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_int_from_string)
```

### get_string_from_float

Parse as float transform to int and cast to string

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_string_from_float)
```

### get_human_input_removed

Remove invalid inputs like

> ...

```python
dataframe["column_x"] = dataframe["column_x"].apply(get_human_input_removed)
```


ftp
-------------
