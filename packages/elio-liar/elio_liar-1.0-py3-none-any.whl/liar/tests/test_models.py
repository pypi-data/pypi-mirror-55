# -*- encoding: utf-8 -*-
import pytest
from liar.model.raw import raw_collection
from liar.model.blurb import blurb_collection
from liar.model.business import business_model
from liar.model.common import common_collection
from liar.model.date import date_collection
from liar.model.float import float_collection
from liar.model.int import int_collection
from liar.model.location import standard_address_model
from liar.model.marketing import marketing_model
from liar.model.personal import personal_model
from liar.model.primitive import primitive_collection
from liar.model.time import time_collection

from liar.ijusthelp import rewrite_dict
from liar.iamaliar import IAmALiar

number_records = 3
maker = IAmALiar(number_records)


class TestClassModels:
    def test_raw(self):
        d = maker.get_data(raw_collection)
        assert len(d) == number_records

    def test_blurb(self):
        d = maker.get_data(blurb_collection)
        assert len(d) == number_records

    def test_business(self):
        d = maker.get_data(business_model)
        assert len(d) == number_records

    def test_common(self):
        d = maker.get_data(common_collection)
        assert len(d) == number_records

    def test_date(self):
        d = maker.get_data(date_collection)
        assert len(d) == number_records

    def test_float(self):
        d = maker.get_data(float_collection)
        assert len(d) == number_records

    def test_int(self):
        d = maker.get_data(int_collection)
        assert len(d) == number_records

    def test_location(self):
        d = maker.get_data(standard_address_model)
        assert len(d) == number_records

    def test_marketing(self):
        d = maker.get_data(marketing_model)
        assert len(d) == number_records

    def test_personal(self):
        d = maker.get_data(personal_model)
        assert len(d) == number_records

    def test_primitive(self):
        d = maker.get_data(primitive_collection)
        assert len(d) == number_records

    def test_time(self):
        d = maker.get_data(time_collection)
        assert len(d) == number_records
