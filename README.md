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

    $ model gen --in preprocessor/data/vectors.pkl \
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

    Han
    Agnand
    Étur
    Vandob
    Finborrin Pooklid
    Fornon oof TookI
    Vand
    Elda
    Inn
    Dírathf Brandybuck
    Mahin
    Frual
    Firnon
    Gron
    Tured erren
    Han
    Ghâdan
    DírSon II
    Mig or
    Wilil II

### George Martin

    Jae Kanot
    Tan drandigg 2
    Cor Lahn
    Wit Gormpndal
    Amrusteites
    Tor of ic taump
    Loiss Wilie Morrsten
    Amrush
    Crigl
    Shomag
    Tyr sr theverry Throprath
    Smone
    Tweilleo
    Mak roundall
    Syvlorthvonk
    Kimmie
    Hea
    Vil Andic
    Rha'Er doust
    Vol Ceampal

### Robert Jordan

    zah
    Bran
    Sanasis
    Mat Aem
    Fla
    Brapan
    Mutr Afilen
    Morien
    Jar
    Sanas
    Grevan
    Mos
    Par
    Yal Anhalis
    Mag
    Nal
    Cya hiel
    Roain
    Carre
    Esi

### Steven Erikson

    Becart
    Fersaune
    Son
    D'allicad
    Kul Rean
    Mousesh
    Sten
    Den
    Cort
    Rilt
    Inn Deart
    Sal
    Thant
    Pan
    Micha E'shoris
    Beca Wor
    Esele
    Bra
    Nit
    Ster

### Brian Jacques

    Sin Doallo
    Craduner
    Vil Rope
    Law
    Bang
    Gogutle
    Scas
    Duf
    Dicale
    Bra
    Tul
    Dager
    Tuk
    Jot
    Ragall
    Brzry
    Karo
    Hore
    Rug
    Vencw

### Frank Herbert

    Ham Vigaty
    Yut Gookbooth
    Phir Heurvoce
    Jai Ghalpawnge
    Ede Bawos
    Hol Cadgett
    Aliant
    Mais Thurighter
    Vandar
    Hoat
    Hia (Haggengol
    Scoch
    Deum
    Ham
    Aur Ajumg
    Hesk II
    Crace
    Xad Toculis
    Paced
    Kanto