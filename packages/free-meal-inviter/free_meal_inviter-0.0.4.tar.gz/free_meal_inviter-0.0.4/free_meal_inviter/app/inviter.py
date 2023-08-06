import enum
import functools
import logging
from typing import Union

from free_meal_inviter.app.parsers import json_parser, csv_parser


logger = logging.getLogger(__name__)


class DataFormat(enum.Enum):
    JSON = 'json'
    CSV = 'csv'


parsers_mapper = {
    DataFormat.JSON: json_parser,
    DataFormat.CSV: functools.partial(csv_parser, fieldnames=('user_id', 'name', 'latitude', 'longitude')),
}


def extract_data(customers_source: str, data_format: Union[str, DataFormat]):
    """
    Extracts customers data from `customers_source` based on `format`.
    If any line does not have the correct format, it will log the error and continue with
    the rest of the lines

    Args:
        customers_source (str): source of the data. It can be a filesystem path.
        data_format (Union[str, :obj:`DataFormat`]): format of data

    Returns:
        Iterable: dictionaries containing the information in `customers_source`
    """
    data_format = DataFormat(data_format)
    try:
        parser = parsers_mapper[data_format]
    except KeyError:
        raise ValueError(f'Invalid format {data_format}')

    with open(customers_source) as f:
        for line in f.readlines():
            try:
                yield parser(line)
            except (ValueError, TypeError) as exc:
                logger.error(f'Error parsing line with format {data_format.value}: {line}')
