# -*- encoding: utf-8 -*-
"""
Business Name suffixes.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import business_type_raw

    # Or from scratch:
    business_type_raw = {
        'name': 'business_type_raw',
        'class': 'igetraw',
        'data': 'business_type',
    }

    data_set = maker.get_data([business_type_raw])

    for row in data_set:
        data = Model()
        data.business_type = row['business_type_raw']
        data.save()

"""

business_type = [
    "Ltd",
    "Plc",
    "& Co",
    "& Partners",
    "Inc",
    "& Son",
    "& Sons",
    "Associated",
    "Corporation",
    "Incorporated",
    "International",
]
