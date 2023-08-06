import csv
import json


def json_parser(elem, **kwargs):
    """
    Deserialize ``elem`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON object) to a Python dictionary.

    Args:
        elem: JSON object in ``str``, ``bytes`` or ``bytearray``
        **kwargs:

    Returns:
        dict: resulting object as dictionary.

    Raises:
        ValueError: If `elem` is not serialized JSON object, for example if
            it is a serialized JSON list.
        TypeError: If `elem` is not a ``str``, ``bytes`` or ``bytearray``.
        JSONDecodeError: If there is something wrong with JSON format.
    """
    obj = json.loads(elem, **kwargs)
    if not isinstance(obj, dict):
        raise ValueError(f'Serialized JSON object was expected, got {type(obj)}')

    return obj


def csv_parser(elem, fieldnames, delimiter=',', **kwargs):
    """
    Parses a row in csv to a Python dictionary based on ``fieldnames`` as its keys

    Args:
        elem (str): row of the csv to be parsed
        delimiter (str): delimiter between values
        fieldnames (list): names of the fields for each column. It will be used for the
            keys in the resulting dictionary
        **kwargs: extra parameters for further configuration in csv reader

    Returns:
        dict: resulting object as dictionary
    """
    reader = csv.DictReader([elem], delimiter=delimiter, fieldnames=fieldnames, **kwargs)
    rows = list(reader)

    if len(rows) != 1:
        raise ValueError(f'Only one row was expected, got {len(rows)}')

    dct = rows[0]
    if any(value is None for value in dct.values()):
        raise ValueError(f'Different number of columns and fieldnames')

    return rows[0]
