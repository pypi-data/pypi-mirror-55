# -*- encoding: utf-8 -*-
"""
A list of words commonly used to suffix animal names. This class is used in
the living thing class to create random, but realistic, common animal names.

**Usage:**

::

    from liar.iamaliar import IAmALiar
    number_records = 10
    maker = IAmALiar(number_records)

    # Use:
    from liar.model.raw import animal_suffix_raw

    # Or from scratch:
    animal_suffix_raw = {
        'name': 'animal_suffix_raw',
        'class': 'igetraw',
        'data': 'animal_suffix',
    }

    data_set = maker.get_data([animal_suffix_raw])

    for row in data_set:
        data = Model()
        data.animal_suffix = row['animal_suffix_raw']
        data.save()

"""

animal_suffix = [
    "Back",
    "Backed",
    "Ball",
    "Balled",
    "Beak",
    "Beaked",
    "Throat",
    "Face",
    "Cupped",
    "Belled",
    "Belly",
    "Bellied",
    "Bells",
    "Cheek",
    "Cheeked",
    "Crowned",
    "Cup",
    "Cups",
    "Eared",
    "Ears",
    "Eyed",
    "Eyes",
    "Faced",
    "Finger",
    "Flax",
    "Flowered",
    "Footed",
    "Haired",
    "Head",
    "Headed",
    "Leaf",
    "Mouth",
    "Mouthed",
    "Nose",
    "Nosed",
    "Plume",
    "San",
    "Shot",
    "Shouldered",
    "Spotted",
    "Tailed",
    "Toed",
    "Toothed",
    "Tooth",
    "Throated",
    "Shoulder",
    "Sanded",
    "Plumed",
    "Feathered",
    "Knee",
    "Kneed",
    "Thighed",
    "Breasted",
    "Breast",
    "Chest",
    "Chested",
    "Laughing",
    "Cackling",
    "Night",
    "Evening",
    "Morning",
    "Heeled",
    "Elbowed",
    "Nailed",
    "Worshiped",
    "Lying",
    "Running",
    "Jumping",
    "Singing",
    "Shouting",
    "Talking",
    "Leafed",
    "Silked",
]
