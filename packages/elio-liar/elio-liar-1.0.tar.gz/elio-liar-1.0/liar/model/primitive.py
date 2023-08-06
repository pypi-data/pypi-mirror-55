# -*- encoding: utf-8 -*-
"""Ready made column definitions for primitive data."""

from liar.ijusthelp import rewrite_dict

iamprimitive = {
    "name": "iamprimitive",
    "class": "iamprimitive",
    "method": "int_list",
    "min": 0,
    "max": 1,
}

int_list = rewrite_dict(
    iamprimitive,
    {"name": "int_list", "method": "int_list", "min": 0, "max": 1000},
)

int_list_1 = rewrite_dict(int_list, {"name": "int_list_1", "min": 1})

dec_list = rewrite_dict(
    iamprimitive,
    {"name": "dec_list", "method": "dec_list", "min": 0, "max": 100000},
)

dec_list_1 = rewrite_dict(dec_list, {"name": "dec_list_1", "min": 1})

time_list = rewrite_dict(
    iamprimitive,
    {
        "name": "time_list",
        "method": "time_list",
        "min": "2017-01-01 00:00:00",
        "max": "2017-01-01 23:59:59",
    },
)

date_list = rewrite_dict(
    iamprimitive,
    {
        "name": "date_list",
        "method": "date_list",
        "min": "2017-01-01",
        "max": "2018-01-01",
    },
)

primary_key_list = rewrite_dict(
    iamprimitive, {"name": "primary_key_list", "method": "primary_key_list"}
)

primitive_collection = [
    iamprimitive,
    int_list,
    int_list_1,
    dec_list,
    dec_list_1,
    time_list,
    date_list,
    primary_key_list,
]
