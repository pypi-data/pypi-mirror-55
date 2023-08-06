from gravtools.constants import Observatory


class TestConstantsObservatory:
    """These tests just assert that the constants don't change unintentionally"""

    def test_observatory(self):
        assert Observatory.LIGOHanford == 'H1'
        assert Observatory.LIGOLivingston == 'L1'
        assert Observatory.VIRGO == 'V1'
