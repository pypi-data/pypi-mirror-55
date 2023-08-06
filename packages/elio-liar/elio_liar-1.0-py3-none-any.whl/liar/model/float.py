# -*- encoding: utf-8 -*-
"""Ready made column definitions for float data."""

from liar.ijusthelp import rewrite_dict
from liar.model.primitive import dec_list

quantum = rewrite_dict(
    dec_list, {"name": "quantum", "max": 0.00001, "min": 0.00009}
)


def float_data(name, min, max):
    return rewrite_dict(quantum, {"name": name, "min": min, "max": max})


fractional = float_data("fractional", 0.000000001, 0.999999999)

grocery_price = float_data("grocery_price", 0.50, 10.00)

consumer_price = float_data("consumer_price", 9.99, 99.99)

gadget_price = float_data("gadget_price", 89.99, 1999.99)

car_price = float_data("car_price", 8000.00, 80000.99)

house_price = float_data("house_price", 160000.00, 1000000.99)

national_gdp = float_data("national_gdp", 1000000000000.00, 1999999999999.99)

float_collection = [
    quantum,
    fractional,
    grocery_price,
    consumer_price,
    gadget_price,
    car_price,
    house_price,
    national_gdp,
]
