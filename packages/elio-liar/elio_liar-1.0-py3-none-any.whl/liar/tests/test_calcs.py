# -*- encoding: utf-8 -*-
import pytest
from liar.iamaliar import IAmALiar


class TestClassCalcs:
    calc_maker = IAmALiar(1)

    def test_calc_add(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 3,
                    "calc": [{"add": 5}],
                }
            ]
        )
        assert d[0]["test_calc"] == 3 + 5

    def test_calc_subtract(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 3,
                    "calc": [{"subtract": 5}],
                }
            ]
        )
        assert d[0]["test_calc"] == 3 - 5

    def test_calc_multiply(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 3,
                    "calc": [{"multiply": 5}],
                }
            ]
        )
        assert d[0]["test_calc"] == 3 * 5

    def test_calc_divide(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 3,
                    "calc": [{"divide": 5}],
                }
            ]
        )
        assert d[0]["test_calc"] == 3 / 5

    def test_calc_format(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 5.012345678,
                    "calc": [{"format": "{:10.2f}"}],
                }
            ]
        )
        assert d[0]["test_calc"] == "      5.01"

    def test_calc_combine(self):
        d = self.calc_maker.get_data(
            [
                {
                    "name": "test_calc",
                    "class": "exact",
                    "data": 3,
                    "calc": [
                        {"multiply": 10},
                        {"add": 2},
                        {"subtract": 5},
                        {"divide": 3},
                    ],
                }
            ]
        )
        assert d[0]["test_calc"] == ((((3 * 10) + 2) - 5) / 3)
