# -*- encoding: utf-8 -*-
"""
Words like Street, Road, Lane, etc, which can be neatly appended to words and
phrases to create realistic address data.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import street_type_raw

    # Or from scratch:
    street_type_raw = {
        'name': 'street_type_raw',
        'class': 'igetraw',
        'data': 'street_type',
    }

    data_set = maker.get_data([street_type_raw])

    for row in data_set:
        data = Model()
        data.subject = row['street_type_raw']['subject']
        data.department = row['street_type_raw']['department']
        data.save()

Create a definition which concatonates a latin word to a street_type to
make a road name

::

    # Use:
    from liar.model.common import nb_space
    from liar.model.int import in_100
    from liar.model.raw import animal_name_raw, street_type_raw

    address1 =   {
        'name': 'address1',
        'class': 'concat',
        'data': [
                in_100,
                nb_space,
                animal_name_raw,
                nb_space,
                street_type_raw,
            ]
    }

    data_set = maker.get_data([address1])

    for row in data_set:
        data = Model()
        data.locality = row['address1']
        data.save()

"""

street_type = [
    "Road",
    "Street",
    "Way",
    "Lane",
    "Avenue",
    "Green",
    "Close",
    "Boulevard",
    "Terrace",
    "Hill",
    "Pen",
    "Park Avenue",
    "Park Road",
    "Heights",
    "Road",
    "Street",
    "Way",
    "Lane",
    "Avenue",
    "Green",
    "Close",
]
