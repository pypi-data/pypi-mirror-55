# -*- encoding: utf-8 -*-
"""Ready made column definitions for common stuff data."""

from liar.ijusthelp import rewrite_dict

from liar.model.raw import (
    animal_name_raw,
    word_prefix_raw,
    english_word_raw,
    word_suffix_raw,
)

pk = {"name": "pk", "class": "pk"}

space = {"name": "space", "class": "exact", "data": " "}

nb_space = {"name": "nb_space", "class": "exact", "data": "&nbsp;"}

animal_name = rewrite_dict(animal_name_raw, {})

compound_word = {
    "name": "compound_word",
    "class": "concat",
    "data": [
        rewrite_dict(word_prefix_raw, {"name": ""}),
        rewrite_dict(english_word_raw, {"name": ""}),
        rewrite_dict(word_suffix_raw, {"name": ""}),
    ],
}

common_collection = [pk, space, nb_space, animal_name, compound_word]
