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

    $ model train --data preprocessor/data/vectors.pkl --save modeler/logs/1

Generate names
--------------

    $ model gen --data preprocessor/data/vectors.pkl \
                --lookup preprocessor/data/lookup.pkl \
                --save modeler/logs/1 \
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

    Qunorthin
    Penny (Baggins) Burrows
    Jase
    Khlair
    Wilan
    Qunaoth
    Elehild
    Argeor
    Haldir
    Romendacil II
    Wilda
    Befgo Baggins II
    Yávien
    Halor
    Inmarë
    Ele Ilúvatar
    Rosa Greenhand
    Galdberry
    Queel
    Sarudas Brandybuck

### George Martin

    Wild man
    Garean Tyrell
    Kinarro
    Orpyle
    Qhrro
    Stiera Seastar
    Kingara
    Xaro Xhoan Daxos
    Rockard Lonmouth
    Ormic Stark
    Pept Pree
    Vaserys IITargaryen
    Joseya Frey
    Inoi
    Lonlsa  Stokeworth
    StmTarly
    Unfana
    Stice King
    Nirven
    Argon I I Targaryen

### Robert Jordan

    Vaealne Garman
    Qiine
    Allon
    Nalomi
    Zanion
    Marem
    Garyn Trranand
    Lacine
    Ha Marran
    Janyde
    Carvele
    Vaeia Connoral
    WiiTomfaine
    Qie
    Romela Cindal
    Teal n
    Vaeia Connoral
    Barlin
    Ferain
    Yakobin

### Steven Erikson

    Nerarkr
    Esesthila
    Xrrloc
    Urenaas
    Reth'D'rek
    Ormal
    Netra
    Wieneck
    Chrpala
    Janalh
    Chraran
    Grenmrog
    Irgast Rend
    Nersaras
    Grnlan
    Serrl
    Reulad Sengar
    Oral
    Yeaki
    Xrddershins

### Brian Jacques

    Thubbaggs
    Dankle
    Urcril
    Orlback
    Darfle
    Mario
    Urtan
    Arrum Vole
    DainpMie Slayer
    Ringar Skurr
    Wilger
    Riona Stinkh
    Daubblewick
    Zailt the Shade
    Zarig
    Ardis
    YooKarr
    Marfo
    Laddtail
    Ord Jarge

### Frank Herbert

    Paudoid Valleck
    Yoette Hagal
    Jenar
    Mares
    Orlop
    Chaopatra
    Wensicia Corrino
    Thelia Ietler
    Paidias Latzko
    Hapar Fen Ajidica
    Yorek Thurr
    Quentin Butler
    Leechine
    Jenets Milam
    Duncmis Atreides
    Narma Cenva/XD
    Uliet
    Wensicia Corrino
    Werdra Butler
    Garusne Itreides