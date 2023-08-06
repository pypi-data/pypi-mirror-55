from typing import Union, Iterable

from free_meal_inviter.app import geo
from free_meal_inviter.app.geo import Coordinates
from free_meal_inviter.app.person import Person


def people_close_to(coordinates: Union[tuple, Coordinates], people: Iterable[Person], distance: float):
    """
    Filters `people` and returns a generator with the :obj:`Person` instances whose coordinates
    are closer than `distance` from `coordinates`

    Args:
        coordinates: coordinates from which it will measure the distance
        people: Iterable of :obj:`Person` to be filtered by the distance
        distance: maximum distance in kilometers

    Returns:
        Iterable of :obj:`Person`: objects whose coordinates are closer than `distance`
            to `coordinates`
    """
    return (p for p in people if geo.great_circle_distance(coordinates, p.coordinates) <= distance)
