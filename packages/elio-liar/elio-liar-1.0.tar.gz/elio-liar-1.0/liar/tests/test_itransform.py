# -*- encoding: utf-8 -*-
import pytest
from slugify import slugify
from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar

from liar.model.raw import (
    ascii_lowercase_raw,
    ascii_uppercase_raw,
    academic_raw,
)

raw = [
    "A",
    "brave,",
    "chance",
    "dance",
    "ended",
    "Fred's",
    "girlfriend",
    "hunt",
    "Ingrid",
    "just",
    "kissed",
    "like",
    "magic!",
    "once",
    "privately",
    "quartered,",
    "Nearby,",
    "romance",
    "secured",
    "the",
    "unfolding",
    "victory",
    "with",
    "X-rated,",
    "youthful",
    "zest.",
]

complex_string = " ".join(raw)

transform_tester = {
    "name": "transform_tester",
    "class": "quicklist",
    "data": [complex_string],
}


class TestClassITransform:

    small_number_records = 1
    transform_maker = IAmALiar(small_number_records)

    def test_transform_upper(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["upper"]})]
        )
        assert complex_string.upper() == d[0]["transform_tester"]

    def test_transform_lower(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["lower"]})]
        )
        assert complex_string.lower() == d[0]["transform_tester"]

    def test_transform_title(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["title"]})]
        )
        assert complex_string.title() == d[0]["transform_tester"]

    def test_transform_chomp(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["chomp"]})]
        )
        assert complex_string[0] == d[0]["transform_tester"]

    def test_transform_capitalize(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["capitalize"]})]
        )
        assert complex_string.capitalize() == d[0]["transform_tester"]

    def test_transform_slugify(self):
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"itransform": ["slugify"]})]
        )
        assert slugify(complex_string) == d[0]["transform_tester"]
