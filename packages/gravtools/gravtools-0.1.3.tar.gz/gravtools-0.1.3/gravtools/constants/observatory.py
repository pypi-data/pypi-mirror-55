"""List of detectors
"""
import enum


class Observatory(str, enum.Enum):
    """Helpful enumeration of observatories for loading strain data"""
    LIGOHanford = 'H1'
    LIGOLivingston = 'L1'
    VIRGO = 'V1'
