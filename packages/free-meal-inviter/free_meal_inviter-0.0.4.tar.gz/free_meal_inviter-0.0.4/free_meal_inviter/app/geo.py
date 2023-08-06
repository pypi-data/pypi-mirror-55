import collections
import math
from typing import Union, Iterable

# IUGG mean earth radius in kilometers, from
# https://en.wikipedia.org/wiki/Earth_radius#Mean_radius.  Using a
# sphere with this radius results in an error of up to about 0.5%.
EARTH_RADIUS = 6371.009


class Coordinates:

    def __init__(self, lat: Union[str, int, float], lng: Union[str, int, float]):
        self._validate_lat(lat)
        self._validate_lng(lng)
        self.lat = float(lat)
        self.lng = float(lng)

    def __getitem__(self, item):
        return tuple(self)[item]

    def __iter__(self):
        return iter((self.lat, self.lng))

    def __eq__(self, other):
        if not isinstance(other, collections.Iterable):
            return NotImplemented
        return tuple(self) == tuple(other)

    @staticmethod
    def _validate_lat(lat):
        if not -90 <= float(lat) <= 90:
            raise ValueError('Latitude cannot be less than -90 or greater than 90')

    @staticmethod
    def _validate_lng(lng):
        if not -180 <= float(lng) <= 180:
            raise ValueError('Longitude cannot be less than -180 or greater than 180')


def great_circle_distance(a: Union[Coordinates, Iterable], b: [Coordinates, Iterable]):
    """
    Calculate the great circle distance between two coordinates in planet Earth
    based on the formula in this Wikipedia Article:
    https://en.wikipedia.org/wiki/Great-circle_distance

    Returns:
        float: great circle distance in kilometers between the two coordinates
    """
    a, b = Coordinates(*a), Coordinates(*b)

    lat1, lng1 = math.radians(a.lat), math.radians(a.lng)
    lat2, lng2 = math.radians(b.lat), math.radians(b.lng)

    sin_lat1, cos_lat1 = math.sin(lat1), math.cos(lat1)
    sin_lat2, cos_lat2 = math.sin(lat2), math.cos(lat2)

    delta_lng = lng2 - lng1

    aux = (sin_lat1 * sin_lat2) + cos_lat1 * cos_lat2 * math.cos(delta_lng)

    # To avoid arccos failing for precision errors
    if aux > 1 and aux - 1 <= 0.000000001:
        aux = 1

    central_angle = math.acos(aux)

    return EARTH_RADIUS * central_angle
