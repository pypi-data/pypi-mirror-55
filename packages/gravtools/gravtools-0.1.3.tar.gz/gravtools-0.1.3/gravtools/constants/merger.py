"""Constants related to mergers in the PyCBC library"""

import enum


class MergerParameters(str, enum.Enum):
    """Useful enumeration of Merger class parameters. These parameters
    get set using setattr, so code inspection doesn't work naturally - this
    Enum can help recall the attributes in an inspectable way.
    """
    ChirpMass = 'mchirp'
    EffInspiralSpin = 'chi_eff'
    FinalMass = 'mfinal'
    FinalSpin = 'a_final'
    LuminosityDistance = 'distance'
    Mass1 = 'mass1'
    Mass2 = 'mass2'
    PeakLuminosity = 'L_peak'
    RadiatedEnergy = 'E_rad'
    Redshift = 'redshift'
    SkySize = 'sky_size'
    SignalNoiseRatio_CWB = 'snr_cwb'
    SignalNoiseRatio_GSTLAL = 'snr_gstlal'
    SignalNoiseRatio_PYCBC = 'snr_pycbc'
