"""Tests for time conversion"""
import datetime

import pytest
from lal import LIGOTimeGPS

from gravtools import time


class TestTime:
    @pytest.fixture(scope='class', autouse=True)
    def gps_time(self):
        return 1187529241

    @pytest.fixture(scope='class', autouse=True)
    def gps_time2(self):
        return LIGOTimeGPS(1187529241)

    def test_gps_to_datetime(self, gps_time, gps_time2):
        assert time.gps_to_datetime(gps_time) == datetime.datetime(2017, 8, 23, 13, 14, 20)
        assert time.gps_to_datetime(gps_time2) == datetime.datetime(2017, 8, 23, 13, 14, 20)
