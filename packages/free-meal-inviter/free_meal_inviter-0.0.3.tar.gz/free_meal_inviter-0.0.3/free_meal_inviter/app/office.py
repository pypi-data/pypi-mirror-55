from typing import Union

from free_meal_inviter.app.geo import Coordinates


class Office:

    def __init__(self, name: str, coordinates: Union[tuple, Coordinates]):
        self.name = name
        self.coordinates = coordinates


dublin_office = Office('Dublin HQ', (53.339428, -6.257664))
