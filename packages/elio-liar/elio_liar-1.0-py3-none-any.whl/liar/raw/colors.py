# -*- encoding: utf-8 -*-
"""
A list of colors.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import colors

    # Or from scratch:
    colors_raw = {
        'name': 'colors_raw',
        'class': 'igetraw',
        'data': 'colors',
    }

    data_set = maker.get_data([colors_raw])

    for row in data_set:
        data = Model()
        data.color = row['colors_raw']
        data.save()

"""

colors = [
    "Aqua",
    "Beige",
    "Bisque",
    "Black",
    "Blue",
    "Brown",
    "Chocolate",
    "Coral",
    "Crimson",
    "Cyan",
    "Fuchsia",
    "Gold",
    "Gray",
    "Green",
    "Indigo",
    "Khaki",
    "Lavender",
    "Lime",
    "Magenta",
    "Maroon",
    "Navy",
    "Olive",
    "Orange",
    "Pink",
    "Plum",
    "Purple",
    "Red",
    "Salmon",
    "Sienna",
    "Silver",
    "Tan",
    "Teal",
    "Tomato",
    "Turquoise",
    "Violet",
    "Wheat",
    "White",
    "Yellow",
]
