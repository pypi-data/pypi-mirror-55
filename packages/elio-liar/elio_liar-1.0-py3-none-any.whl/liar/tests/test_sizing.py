# -*- encoding: utf-8 -*-
import pytest
from liar.ijusthelp import rewrite_dict, get_single_from_list
from liar.iamaliar import IAmALiar

from liar.model.raw import ainu_raw


class TestClassSizing:
    def test_sizing_record(self):
        number_records = 1
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        assert len(d) == number_records

    def test_sizing_records(self):
        number_records = 10000
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        assert len(d) == number_records

    def test_sizing_get_single(self):
        number_records = 10000
        maker = IAmALiar(number_records)
        d = maker.get_data([ainu_raw])
        item = get_single_from_list(d)
        assert isinstance(item["ainu_raw"], str)
