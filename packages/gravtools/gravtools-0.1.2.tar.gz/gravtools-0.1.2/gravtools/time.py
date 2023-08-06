"""Time conversion utilities"""
import datetime
import typing

from astropy import time
from lal import LIGOTimeGPS

def gps_to_datetime(gps_time: typing.Union[float, LIGOTimeGPS]) -> datetime.datetime:
    """Convert GPS to datetime, helper function around the astropy Time api

    Args:
        gps_time:
            float or LIGOTimeGPS, the GPS time

    Returns:
        datetime.datetime, the default python datetime format
    """
    if isinstance(gps_time, LIGOTimeGPS):
        gps_time = float(gps_time)
    gps = time.Time(gps_time, format='gps')
    return gps.to_datetime()
