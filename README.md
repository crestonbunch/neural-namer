# Neural Namer

A character RNN that learns how to emulate the styles of names of different
fantasy authors.

Demo: https://crestonbunch.github.io/neural-namer-demo/

# Usage

Recommended process is to setup a Python Virtual environment.

## First time setup

This will create a Python virtual environment, and install the necessary
packages only for this project.

    $ pip install virtualenv
    $ virtualenv -p /usr/bin/python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py develop

## Running from the virtual environment

Make sure you run the commands from inside the virtual environment, once the
virtual environment is created, you can enter it with:

    $ source venv/bin/activate

## Scrape data

    $ crawl wikia --out crawler/wikia/data/names.csv

## Train the model

    $ model train --data crawler/wikia/data/names.csv --save modeler/logs/1

## Generate names

    $ model gen --save modeler/logs/1 \
                --data crawler/wikia/data/names.csv \
                --author "Tolkien"

Replace 'Tolkien' with another author:

* Tolkien (Lord of the Rings)
* George Martin (A Song of Ice and Fire)
* Robert Jordan (Wheel of Time)
* Steven Erikson (Malazan)
* Brian Jacques (Redwall)
* Frank Herbert (Dune)
* Andrzej Sapkowski (The Witcher)

## Web interface

TODO: currently only networks with one LSTM cell are supported by the web interface.
Don't try to migrate a model with more than one LSTM cell!
It might work, but your model certainly won't generate correct outputs.

To migrate Tensorflow models into the web directory:

    $ python scripts/migrate.py \
        --data crawler/wikia/data/names.csv\
        --checkpoint modeler/logs/1/model.ckpt-5600

Replace the `-5600` suffix with the last checkpoint in your directory

To run the web interface

    $ cd web/
    $ yarn install
    $ webpack-dev-server
    $ firefox localhost:8080

There is no web backend, which means you can serve the web interface
from any service that can serve static HTML, CSS, and JavaScript. E.g. GitHub pages.
