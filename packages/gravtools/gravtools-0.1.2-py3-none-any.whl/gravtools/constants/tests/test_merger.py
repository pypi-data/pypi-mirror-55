from gravtools.constants import MergerParameters


class TestConstantsMerger:
    """These tests just assert that the constants don't change unintentionally"""

    def test_merger_parameters(self):
        assert MergerParameters.ChirpMass == 'mchirp'
        assert MergerParameters.EffInspiralSpin == 'chi_eff'
        assert MergerParameters.FinalMass == 'mfinal'
        assert MergerParameters.FinalSpin == 'a_final'
        assert MergerParameters.LuminosityDistance == 'distance'
        assert MergerParameters.Mass1 == 'mass1'
        assert MergerParameters.Mass2 == 'mass2'
        assert MergerParameters.PeakLuminosity == 'L_peak'
        assert MergerParameters.RadiatedEnergy == 'E_rad'
        assert MergerParameters.Redshift == 'redshift'
        assert MergerParameters.SkySize == 'sky_size'
        assert MergerParameters.SignalNoiseRatio_CWB == 'snr_cwb'
        assert MergerParameters.SignalNoiseRatio_GSTLAL == 'snr_gstlal'
        assert MergerParameters.SignalNoiseRatio_PYCBC == 'snr_pycbc'
