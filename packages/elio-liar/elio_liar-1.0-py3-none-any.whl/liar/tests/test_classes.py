# -*- encoding: utf-8 -*-
import pytest
from liar.ijusthelp import rewrite_dict, get_single_from_list
from liar.iamaliar import IAmALiar


class TestClassClasses:
    def test_exact_list(self):
        number_records = 100
        maker = IAmALiar(number_records)
        data = maker.get_data(
            [{"name": "fieldname", "class": "exact", "data": "pie"}]
        )
        assert 100 == len(data)
        assert {"pie"} == set([f["fieldname"] for f in data])

    def test_quick_list(self):
        number_records = 100
        maker = IAmALiar(number_records)
        data = maker.get_data(
            [
                {
                    "name": "fieldname",
                    "class": "quicklist",
                    "data": ["x", "y", "z"],
                }
            ]
        )
        assert {"x", "y", "z"} == set([f["fieldname"] for f in data])

    def test_toothpaste_list(self):
        number_records = 10
        maker = IAmALiar(number_records)
        data = maker.get_data(
            [
                {
                    "name": "fieldname",
                    "class": "toothpaste",
                    "data": ["x", "y", "z"],
                }
            ]
        )
        assert ["x", "y", "z", "x", "y", "z", "x", "y", "z", "x"] == [
            f["fieldname"] for f in data
        ]
