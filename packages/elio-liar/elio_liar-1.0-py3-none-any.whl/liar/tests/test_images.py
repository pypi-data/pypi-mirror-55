# -*- encoding: utf-8 -*-
import os
import pytest
from liar.iamaliar import IAmALiar
from liar.model.raw import animal_raw, geo_location_raw


maker = IAmALiar(1)


class TestClassModels:
    def test_animal_raw_images(self):
        d = maker.get_data([animal_raw])
        # Test that the absolute path to the image is relatively accurate
        path = d[0]["animal_raw"]["images"]["drawing"]
        print(path)
        assert os.path.abspath(".").split("/")[0:7] == path.split("/")[0:7]
        assert ["liar", "liar", "images", "animal"] == path.split("/")[-5:-1]

    def test_geo_location_raw_images(self):
        d = maker.get_data([geo_location_raw])
        # Test that the absolute path to the image is relatively accurate
        path = d[0]["geo_location_raw"]["images"]["flag"]
        assert os.path.abspath(".").split("/")[0:7] == path.split("/")[0:7]
        assert ["liar", "liar", "images", "flag"] == path.split("/")[-5:-1]
