"""Tests for merger"""

import pytest
from pycbc import catalog

from gravtools import merger, MergerParameters


class TestMerger:
    @pytest.fixture(scope='class', autouse=True)
    def m(self):
        return catalog.Merger('GW150914')

    def test_name(self, m):
        assert merger.name(m) == 'GW150914'

    def test_summary(self, m):
        assert merger.summary(m) == 'Merger[GW150914](Mass1=35.6, Mass2=30.6, FinalSpin=0.69)'
        assert merger.summary(m, parameters=[MergerParameters.Redshift]) == 'Merger[GW150914](Redshift=0.09)'
