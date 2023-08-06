import os
from os import path
import sys

import click

# To avoid having to set PYTHONPATH manually, or remove this module from the package
sys.path.append(path.join(path.abspath(path.dirname(__file__)), os.pardir))

from free_meal_inviter.app import services
from free_meal_inviter.app.inviter import extract_data, parsers_mapper
from free_meal_inviter.app.office import dublin_office
from free_meal_inviter.app.person import Person


@click.command()
@click.option('-f', '--data-format', help='Format of input data', default='json',
              type=click.Choice([p.value for p in parsers_mapper.keys()]))
@click.option('-d', '--distance', help='Maximum distance for a customer to be invited', default=100,
              type=float)
@click.argument('customers_source')
def main(data_format, distance, customers_source):
    customers = (Person.from_dict(item) for item in extract_data(customers_source, data_format))
    close_customers = services.people_close_to(dublin_office.coordinates, customers, distance)
    for customer in sorted(close_customers, key=lambda c: c.user_id):
        print(f'{customer.user_id} - {customer.name}')

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
