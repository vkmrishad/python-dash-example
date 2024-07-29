# python-dash-example
Python Dash With Bootstrap

## Clone

    git clone https://github.com/vkmrishad/python-dash-example.git
    or
    git clone git@github.com:vkmrishad/python-dash-example.git

## System dependencies

* [Python: 3.10+](https://www.python.org/downloads/)
* SQLite3

## Environment and Package Management
Install [Poetry](https://python-poetry.org/)

    $ pip install poetry
    or
    $ pip3 install poetry

Activate or Create Env

    $ poetry shell

Install Packages from Poetry

    $ poetry install

## Add fixer data to the database

    $ python -m src.db.fixture
    or
    $ python3 -m src.db.fixture

## Runserver
    $ python app.py
    or
    $ python3 app.py

## Sample Excel xls file available in the directory
    $ cd src/db/data/(GB) Sample - EU Superstore.xls
