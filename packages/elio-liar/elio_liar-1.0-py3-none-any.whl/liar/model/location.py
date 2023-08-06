# -*- encoding: utf-8 -*-
"""Ready made column definitions for location data."""

from liar.ijusthelp import rewrite_dict
from liar.model.common import nb_space
from liar.model.int import in_100, city_populations
from liar.model.primitive import int_list
from liar.model.raw import (
    ainu_raw,
    latin_raw,
    animal_name_raw,
    street_type_raw,
    district_suffix_raw,
    surname_raw,
    geo_location_raw,
)

posh_address1 = {
    "name": "posh_address1",
    "class": "concat",
    "data": [
        {"class": "exact", "data": "The ", "splutter": 20},
        nb_space,
        surname_raw,
    ],
}


address1 = {
    "name": "address1",
    "class": "concat",
    "data": [in_100, nb_space, animal_name_raw, nb_space, street_type_raw],
}

address2 = {
    "name": "locality",
    "class": "concat",
    "itransform": ["capitalize"],
    "data": [ainu_raw, district_suffix_raw],
}

locality = {
    "name": "locality",
    "class": "concat",
    "itransform": ["capitalize"],
    "data": [latin_raw, district_suffix_raw],
}

geo_location = geo_location_raw

post_code = rewrite_dict(
    int_list, {"name": "post_code", "min": 10000, "max": 999999}
)

standard_address_model = [address1, address2, locality, geo_location, post_code]

posh_address_model = [
    posh_address1,
    address2,
    locality,
    geo_location,
    post_code,
]
