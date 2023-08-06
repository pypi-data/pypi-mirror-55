# -*- encoding: utf-8 -*-
"""
A list of words commonly used to suffix urban and country locations.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import district_suffix_raw

    # Or from scratch:
    district_suffix_raw = {
        'name': 'district_suffix_raw',
        'class': 'igetraw',
        'data': 'district_suffix',
    }

    data_set = maker.get_data([district_suffix_raw])

    for row in data_set:
        data = Model()
        data.district_suffix = row['district_suffix_raw']
        data.save()

Create a definition which concatonates a latin word to a district_suffix

::

    latin_raw = {
        'name': 'latin_raw',
        'class': 'igetraw',
        'data': 'latin',
    }

    locality = {
        'name': 'locality_field',
        'class': 'concat',
        'itransform': ['capitalize'],
        'data': [latin_raw, district_suffix_raw],
    }

    data_set = maker.get_data([locality])

    for row in data_set:
        data = Model()
        data.locality = row['locality']
        data.save()

"""

district_suffix = [
    "dale",
    "field",
    "ham",
    "water",
    "wood",
    " Bridge",
    " by the River",
    " City",
    " Climbs",
    " Cold",
    " Common",
    " Dales",
    " Dell",
    " District",
    " East",
    " Field",
    " Flats",
    " Farm",
    " Knowles",
    " Farms",
    " Heights",
    " Hills",
    "dale",
    "field",
    "ham",
    "water",
    "wood",
    " in the Hole",
    " in the Wood",
    " Knarl",
    " Knot",
    " Mole",
    " North",
    " North East",
    " North West",
    "dale",
    "field",
    "ham",
    "water",
    "wood",
    " off the Track",
    " on the Dell",
    " on the Hill",
    " Park",
    " Plains",
    " Rains",
    " River",
    " South",
    " South East",
    " South West",
    " Springs",
    " Valley",
    " Waters",
    " West",
    " Woods",
    "dale",
    "field",
    "ham",
    "water",
    "wood",
]
