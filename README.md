# Neural Namer

A character RNN that learns how to emulate the styles of names of different
fantasy authors.

Implemented in TensorFlow with RNN cells based on the following paper:
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/rnn_ctxt.pdf

Usage
=====

Recommended process is to setup a Python Virtual environment.

First time setup
----------------

This will create a Python virtual environment, and install the necessary
packages only for this project.

    $ pip install virtualenv
    $ virtualenv -p /usr/bin/python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py develop

Running from the virtual environment
------------------------------------

Make sure you run the commands from inside the virtual environment, once the
virtual environment is created, you can enter it with:

    $ source venv/bin/activate

Scrape data
-----------

    $ crawl wikia --out crawler/wikia/data/names.pkl

Preprocess data
---------------

    $ preprocess --in crawler/wikia/data/names.pkl \
                 --out preprocessor/data/vectors.pkl \
                 --lookup preprocessor/data/lookup.pkl

Train the model
---------------

    $ model train --in preprocessor/data/vectors.pkl --log modeler/logs/1

Generate names
--------------

    $ model train --in preprocessor/data/vectors.pkl \
                  --lookup preprocessor/data/lookup.pkl \
                  --log modeler/logs/1 \
                  --author "Tolkien"

Replace 'Tolkien' with another author:

* Tolkien
* George Martin
* Robert Jordan
* Steven Erikson
* Brian Jacques
* Frank Herbert

Unfinished work
===============

* Collect more training data
* Create a web interface
* Explore alternative models

Example output
==============

### Tolkien

    Frais
    Laurin Took Cretor Higmar
    Frise Toreel
    Grad
    Ta Brand
    Nimet
    Ise
    Brag
    Her
    Erel
    Heeldos
    Grod Rotion
    Báln Foolmut
    Dímandun
    Ara
    Indil
    Hamhâno
    Leur
    Ta chang
    Ner

### George Martin

    Nug /'Daldon
    Rhen
    Nur
    Drey Coptery
    Lyanangler
    Bar
    Denn KerLtan
    Dan Lalkornim
    Kissscot
    Jaen Ryme Larlth
    Sten Loot mongears Tybutanf
    Brondee
    Tahrenor
    Drim Wophis Dury of Do
    Dou Dilatter
    Drigori
    Mys
    Vion Graz
    King
    Dorlo

### Robert Jordan

    Carion
    Tira
    Kie Sedaridos
    Haak
    Sular
    Carien
    Cloman
    Elon Homa Argarin
    ellin Stane
    Ban Avarat
    Suloul
    Atrak
    Shadin
    Masa
    Muar
    Jho
    Muan Gadewial
    Eyl
    Wiam Elaivi
    Alia Karald

### Steven Erikson

    Shan
    Lun
    Rala
    Hur
    Far
    Rala
    Lusrin
    Pule prrich
    Buder
    Udder
    Nathen
    Hern Senvin
    Vethen
    Mas Dog
    Miss Rucche
    Mes
    Sham
    Had Stad
    Trae
    Prem

### Brian Jacques

    Gree
    Pety
    Craladge
    Rug
    Rig
    Bula Frron
    Gree Larl
    Nur
    Frak
    Grin
    Ruf
    Gur  hange
    For
    Bara
    Gus Swong
    Taic
    Sill
    Chaisiood
    Dree
    Witer Speny

### Frank Herbert

    Aleeg Ifla
    Kans
    Ham Naj
    Iaba Forrow
    Crollung/XD
    Feda
    Madton Corfloo
    Shan torlugon
    Gitter
    Giiss
    Zolint
    Heva
    Vinar Forkino
    Ham Ala
    Cooneth
    Mugandig
    Hema
    Ham Bonkilor Toliennone
    Pate Alacan
    Gana Rtovil
