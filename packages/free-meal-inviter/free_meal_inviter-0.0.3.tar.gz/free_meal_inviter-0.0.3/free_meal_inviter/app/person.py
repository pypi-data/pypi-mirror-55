from typing import Union

from free_meal_inviter.app.geo import Coordinates


class Person:

    def __init__(self, user_id, name, coordinates: Union[tuple, Coordinates]):
        self.user_id = user_id
        self.name = name
        self.coordinates = Coordinates(*coordinates)

    @classmethod
    def from_dict(cls, dct: dict):
        return cls(int(dct['user_id']), dct['name'], (dct['latitude'], dct['longitude']))
