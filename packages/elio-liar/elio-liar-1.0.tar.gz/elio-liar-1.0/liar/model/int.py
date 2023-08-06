# -*- encoding: utf-8 -*-
"""Ready made column definitions for integer data."""

from liar.ijusthelp import rewrite_dict
from liar.model.primitive import int_list

zero_or_one = rewrite_dict(
    int_list, {"name": "zero_or_one", "min": 0, "max": 1}
)


def int_data(name, min, max):
    return rewrite_dict(zero_or_one, {"name": name, "min": min, "max": max})


one_or_two = int_data("one_or_two", 1, 2)

in_3 = int_data("in_3", 1, 3)
in_4 = int_data("in_4", 1, 4)
in_5 = int_data("in_5", 1, 5)
dice = int_data("dice", 1, 6)
in_7 = int_data("in_7", 1, 7)
in_8 = int_data("in_8", 1, 8)
in_9 = int_data("in_9", 1, 9)

in_10 = int_data("in_10", 1, 10)
in_11 = int_data("in_11", 1, 11)
dozen = int_data("dozen", 1, 12)
in_20 = int_data("in_20", 1, 10)
in_24 = int_data("in_24", 1, 24)
in_50 = int_data("in_50", 1, 50)

in_100 = int_data("in_100", 1, 100)
in_1000 = int_data("in_1000", 1, 1000)
in_10000 = int_data("in_10000", 1, 10000)

town_populations = int_data("in_10", 2500, 50000)
city_populations = int_data("in_10", 50000, 20000000)
country_populations = int_data("in_10", 10000000, 1500000000)

stars_in_galaxy = int_data("in_10", 300000000000, 3000000000000)

int_collection = [
    zero_or_one,
    one_or_two,
    in_3,
    in_4,
    in_5,
    dice,
    in_7,
    in_8,
    in_9,
    in_10,
    in_11,
    dozen,
    in_20,
    in_24,
    in_50,
    in_100,
    in_1000,
    in_10000,
    town_populations,
    city_populations,
    country_populations,
    stars_in_galaxy,
]
