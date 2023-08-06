"""Tests for time conversion"""
import datetime

import pytest
from gravtools import time


class TestTime:
    @pytest.fixture(scope='class', autouse=True)
    def gps_time(self):
        return 1187529241

    def test_gps_to_datetime(self, gps_time):
        assert time.gps_to_datetime(gps_time) == datetime.datetime(2017, 8, 23, 13, 14, 20)
