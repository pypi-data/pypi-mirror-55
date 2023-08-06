"""Utilities for PyCBC Merger

"""
import typing

from pycbc.catalog import Merger

from gravtools import MergerParameters

_FILES_ATTR = 'files'
_NAME_ATTR = 'eventName'
DEFAULT_SUMMARY_PARAMETERS = [
    MergerParameters.Mass1,
    MergerParameters.Mass2,
    MergerParameters.FinalSpin,
]


def name(m: Merger) -> str:
    """Helper function for extracting a Merger's name. This function
    relies on implementation details of PyCBC.Merger, which is unfortunate.
    However, the object has no helpful __repr__ implementation, so we
    are forced to inspect the attributes here.

    Args:
        m:
            Merger, the object from which to extract the name

    Returns:
        str, the name of the merger
    """
    return m.data[_FILES_ATTR][_NAME_ATTR]


def summary(m: Merger, parameters: typing.List[MergerParameters] = DEFAULT_SUMMARY_PARAMETERS) -> str:
    """A summary string of a Merger object

    Args:
        m:
            Merger, the merger to be summarized

    Returns:
        str, the summary string of the merger
        Sample: Merger[GW150914](Mass1=35.6, Mass2=30.6, FinalSpin=0.69)
    """
    return 'Merger[{name}]({parameters})'.format(name=name(m),
                                                 parameters=', '.join(
                                                     '{}={}'.format(p.name, m.median1d(p)) for p in parameters))
