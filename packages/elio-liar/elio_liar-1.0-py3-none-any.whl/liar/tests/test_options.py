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
    "hunt.",
    "Ingrid",
    "just",
    "kissed",
    "like",
    "magic!",
    "Nearby,",
    "once",
    "privately",
    "quartered,",
    "romance",
    "secured",
    "the",
    "unfolding",
    "victory",
    "with",
    "xrated,",
    "youthful",
    "zest.",
]


complex_string = " ".join(raw)

transform_tester = {
    "name": "transform_tester",
    "class": "quicklist",
    "data": [complex_string],
}


class TestClassOptions:

    large_number_records = 10000
    transform_maker = IAmALiar(large_number_records)

    def test_options_splutter(self):
        percent = 50
        target = self.large_number_records * (percent / 100)
        leeway = self.large_number_records * (10 / 100)  #%
        d = self.transform_maker.get_data(
            [rewrite_dict(transform_tester, {"splutter": percent})]
        )
        d_not_blank = [item for item in d if item["transform_tester"]]
        assert len(d_not_blank) > (target - leeway) and len(d_not_blank) < (
            target + leeway
        )

    def test_options_filter(self):
        d = self.transform_maker.get_data([academic_raw])
        assert {"Arts", "Business", "Science"} == set(
            [item["academic_raw"]["department"] for item in d]
        )

        d = self.transform_maker.get_data(
            [
                rewrite_dict(
                    academic_raw,
                    {"filters": {"department": ["Arts", "Science"]}},
                )
            ]
        )
        assert {"Arts", "Science"} == set(
            [item["academic_raw"]["department"] for item in d]
        )

    def test_options_multi_filter(self):
        d = self.transform_maker.get_data(
            [
                {
                    "name": "p1",
                    "class": "igetraw",
                    "data": "person",
                    "filters": {"sex": ["female"], "title": ["Mrs", "Dr"]},
                }
            ]
        )
        assert {"female"} == set([item["p1"]["sex"] for item in d])
        assert {"Dr", "Mrs"} == set([item["p1"]["title"] for item in d])

    def test_options_remove(self):
        resp = "NOSUCHCOLUMN!"
        d = self.transform_maker.get_data(
            [
                ascii_lowercase_raw,
                rewrite_dict(ascii_uppercase_raw, {"remove": True}),
            ]
        )
        assert d[0].get("ascii_uppercase_raw", resp) == resp


class TestClassFlatten:
    def test_flatten_column(self):
        number_records = 1
        maker = IAmALiar(number_records)
        data = maker.get_data(
            [
                {
                    "name": "academic",
                    "class": "igetraw",
                    "data": "academic",
                    "flatten": True,
                }
            ]
        )
        assert 1 == len(data)
        assert 2 == len(data[0].keys())
        assert {"academic_department", "academic_subject"} == set(
            data[0].keys()
        )
