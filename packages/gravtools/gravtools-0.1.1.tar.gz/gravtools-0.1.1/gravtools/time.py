"""Time conversion utilities"""
import datetime

from astropy import time

def gps_to_datetime(gps_time: float) -> datetime.datetime:
    """Convert GPS to datetime, helper function around the astropy Time api

    Args:
        gps_time:
            float, the GPS time

    Returns:
        datetime.datetime, the default python datetime format
    """
    gps = time.Time(gps_time, format='gps')
    return gps.to_datetime()
