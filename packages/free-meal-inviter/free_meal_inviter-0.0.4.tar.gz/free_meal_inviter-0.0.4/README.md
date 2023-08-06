Free meal inviter
===============================


Overview
--------

Invite friends around you for a free meal.

Installation / Usage
--------------------

Compatible with Python >= 3.6.

To install use pip:

    $ pip install free_meal_inviter


Or clone the repo:

    $ git clone https://github.com/bertucho/free_meal_inviter.git
    $ python3 setup.py install

Usage
-------

    $ free_meal_inviter [OPTIONS] CUSTOMERS_SOURCE

    Options:
      -f, --data-format [json|csv]  Format of input data
      -d, --distance FLOAT          Maximum distance for a customer to be invited
      --help                        Show this message and exit.

Example
-------
For a plain file containing json data:

    free_meal_inviter data/customers.txt

For a csv file:

    free_meal_inviter --data-format=csv data/customers.csv

Testing
-------

To execute tests, first install the development requirements:
    
    $ git clone https://github.com/bertucho/free_meal_inviter.git
    $ pip install -r requirements_dev.txt
    
Execute tests:

    $ python3 -m unittest
