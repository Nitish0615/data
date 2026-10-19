# distance_utils.py

import math


def calculate_distance_miles(lat1, lon1, lat2, lon2):
    """
    Straight-line distance using Haversine formula.
    Returns miles.
    """

    # Convert degrees to radians
    rlat1 = math.radians(lat1)
    rlon1 = math.radians(lon1)
    rlat2 = math.radians(lat2)
    rlon2 = math.radians(lon2)

    dlat = rlat2 - rlat1
    dlon = rlon2 - rlon1

    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Earth radius in miles
    R = 3958.8
    distance = R * c
    return distance
